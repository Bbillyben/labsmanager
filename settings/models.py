
"""  Credit : Inventree https://github.com/inventree/InvenTree 
### Largely copyed from Inventree : https://github.com/Inventree/Inventree/blob/b50a6826efd8a8e832da43fed0239558fd473e17/LabsManager/common/models.py
"""
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.sites.models import Site
# from django.core.cache import cache
from django.core.exceptions import AppRegistryNotReady, ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    URLValidator, DecimalValidator)
from django.db import models, transaction
from django.db.utils import IntegrityError, OperationalError
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

import labsmanager.utils
import labsmanager.ready
from labsmanager.models_utils import PERCENTAGE_VALIDATOR

from labsmanager.settings import LANGUAGES
from labsmanager.themes import LabTheme

from decimal import Decimal

class BaseLabsManagerSetting(models.Model):
    """An base LabsManagerSetting object is a key:value pair used for storing single values (e.g. one-off settings values)."""

    SETTINGS = {}

    class Meta:
        """Meta options for BaseLabsManagerSetting -> abstract stops creation of database entry."""

        abstract = True

    def save(self, *args, **kwargs):
        """Enforce validation and clean before saving."""
        self.key = str(self.key).upper()


        self.clean(**kwargs)
        self.validate_unique(**kwargs)

        super().save()

        # Get after_save action
        setting = self.get_setting_definition(self.key, *args, **kwargs)
        after_save = setting.get('after_save', None)

        # Execute if callable
        if callable(after_save):
            after_save(self)

    @classmethod
    def allValues(cls, user=None, exclude_hidden=False):
        """Return a dict of "all" defined global settings.
        This performs a single database lookup,
        and then any settings which are not *in* the database
        are assigned their default values
        """
        results = cls.objects.all()

        # Optionally filter by user
        if user is not None:
            results = results.filter(user=user)

        # Query the database
        settings = {}

        for setting in results:
            if setting.key:
                settings[setting.key.upper()] = setting.value

        # Specify any "default" values which are not in the database
        for key in cls.SETTINGS.keys():

            if key.upper() not in settings:
                settings[key.upper()] = cls.get_setting_default(key)

            if exclude_hidden:
                hidden = cls.SETTINGS[key].get('hidden', False)

                if hidden:
                    # Remove hidden items
                    del settings[key.upper()]

        for key, value in settings.items():
            validator = cls.get_setting_validator(key)

            if cls.is_protected(key):
                value = '***'
            elif cls.validator_is_bool(validator):
                value = labsmanager.utils.str2bool(value)
            elif cls.validator_is_int(validator):
                try:
                    value = int(value)
                except ValueError:
                    value = cls.get_setting_default(key)

            settings[key] = value

        return settings

    def get_kwargs(self):
        """Construct kwargs for doing class-based settings lookup, depending on *which* class we are.
        This is necessary to abtract the settings object
        from the implementing class (e.g plugins)
        Subclasses should override this function to ensure the kwargs are correctly set.
        """
        return {}

    @classmethod
    def get_setting_definition(cls, key, **kwargs):
        """Return the 'definition' of a particular settings value, as a dict object.
        - The 'settings' dict can be passed as a kwarg
        - If not passed, look for cls.SETTINGS
        - Returns an empty dict if the key is not found
        """
        settings = kwargs.get('settings', cls.SETTINGS)

        key = str(key).strip().upper()

        if settings is not None and key in settings:
            return settings[key]
        else:
            return {}

    @classmethod
    def get_setting_name(cls, key, **kwargs):
        """Return the name of a particular setting.
        If it does not exist, return an empty string.
        """
        setting = cls.get_setting_definition(key, **kwargs)
        return setting.get('name', '')

    @classmethod
    def get_setting_description(cls, key, **kwargs):
        """Return the description for a particular setting.
        If it does not exist, return an empty string.
        """
        setting = cls.get_setting_definition(key, **kwargs)

        return setting.get('description', '')

    @classmethod
    def get_setting_units(cls, key, **kwargs):
        """Return the units for a particular setting.
        If it does not exist, return an empty string.
        """
        setting = cls.get_setting_definition(key, **kwargs)

        return setting.get('units', '')

    @classmethod
    def get_setting_validator(cls, key, **kwargs):
        """Return the validator for a particular setting.
        If it does not exist, return None
        """
        setting = cls.get_setting_definition(key, **kwargs)

        return setting.get('validator', None)

    @classmethod
    def get_setting_default(cls, key, **kwargs):
        """Return the default value for a particular setting.
        If it does not exist, return an empty string
        """
        setting = cls.get_setting_definition(key, **kwargs)

        default = setting.get('default', '')
        if callable(default):
            return default()
        return default

    @classmethod
    def get_setting_choices(cls, key, **kwargs):
        """Return the validator choices available for a particular setting."""
        setting = cls.get_setting_definition(key, **kwargs)

        choices = setting.get('choices', None)
        if callable(choices):
            # Evaluate the function (we expect it will return a list of tuples...)
            return choices()
        
        return choices

    @classmethod
    def get_setting_object(cls, key, **kwargs):
        """Return an LabsManagerSetting object matching the given key.
        - Key is case-insensitive
        - Returns None if no match is made
        First checks the cache to see if this object has recently been accessed,
        and returns the cached version if so.
        """
        key = str(key).strip().upper()

        filters = {
            'key__iexact': key,
        }

        # Filter by user
        user = kwargs.get('user', None)

        if user is not None:
            filters['user'] = user

        # # Filter by plugin
        # plugin = kwargs.get('plugin', None)

        # if plugin is not None:
        #     from plugin import LabsManagerPlugin

        #     if issubclass(plugin.__class__, LabsManagerPlugin):
        #         plugin = plugin.plugin_config()

        #     filters['plugin'] = plugin
        #     kwargs['plugin'] = plugin

        # Filter by method
        method = kwargs.get('method', None)

        if method is not None:
            filters['method'] = method


        try:
            settings = cls.objects.all()
            setting = settings.filter(**filters).first()
        except (ValueError, cls.DoesNotExist):
            setting = None
        except (IntegrityError, OperationalError):
            setting = None

        # Setting does not exist! (Try to create it)
        if not setting:

            # Unless otherwise specified, attempt to create the setting
            create = kwargs.get('create', True)

            # Prevent creation of new settings objects when importing data
            if labsmanager.ready.isImportingData() or not labsmanager.ready.canAppAccessDatabase(allow_test=True):
                create = False

            if create:
                # Attempt to create a new settings object
                setting = cls(
                    key=key,
                    value=cls.get_setting_default(key, **kwargs),
                    **kwargs
                )

                try:
                    # Wrap this statement in "atomic", so it can be rolled back if it fails
                    with transaction.atomic():
                        setting.save(**kwargs)
                except (IntegrityError, OperationalError):
                    # It might be the case that the database isn't created yet
                    pass


        return setting

    @classmethod
    def get_setting(cls, key, backup_value=None, **kwargs):
        """Get the value of a particular setting.
        If it does not exist, return the backup value (default = None)
        """
        # If no backup value is specified, atttempt to retrieve a "default" value
        if backup_value is None:
            backup_value = cls.get_setting_default(key, **kwargs)

        setting = cls.get_setting_object(key, **kwargs)

        if setting:
            value = setting.value

            # Cast to boolean if necessary
            if setting.is_bool():
                value = labsmanager.utils.str2bool(value)

            # Cast to integer if necessary
            if setting.is_int():
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    value = backup_value

        else:
            value = backup_value

        return value

    @classmethod
    def set_setting(cls, key, value, change_user, create=True, **kwargs):
        """Set the value of a particular setting. If it does not exist, option to create it.
        Args:
            key: settings key
            value: New value
            change_user: User object (must be staff member to update a core setting)
            create: If True, create a new setting if the specified key does not exist.
        """
        if change_user is not None and not change_user.is_staff:
            return

        filters = {
            'key__iexact': key,
        }

        user = kwargs.get('user', None)
        plugin = kwargs.get('plugin', None)

        if user is not None:
            filters['user'] = user

        if plugin is not None:
            from plugin import LabsManagerPlugin

            if issubclass(plugin.__class__, LabsManagerPlugin):
                filters['plugin'] = plugin.plugin_config()
            else:
                filters['plugin'] = plugin

        try:
            setting = cls.objects.get(**filters)
        except cls.DoesNotExist:

            if create:
                setting = cls(key=key, **kwargs)
            else:
                return

        # Enforce standard boolean representation
        if setting.is_bool():
            value = labsmanager.utils.str2bool(value)

        setting.value = str(value)
        setting.save()

    key = models.CharField(max_length=50, blank=False, unique=False, help_text=_('Settings key (must be unique - case insensitive)'))

    value = models.CharField(max_length=200, blank=True, unique=False, help_text=_('Settings value'))

    @property
    def name(self):
        """Return name for setting."""
        return self.__class__.get_setting_name(self.key, **self.get_kwargs())

    @property
    def default_value(self):
        """Return default_value for setting."""
        return self.__class__.get_setting_default(self.key, **self.get_kwargs())

    @property
    def description(self):
        """Return description for setting."""
        return self.__class__.get_setting_description(self.key, **self.get_kwargs())

    @property
    def units(self):
        """Return units for setting."""
        return self.__class__.get_setting_units(self.key, **self.get_kwargs())

    def clean(self, **kwargs):
        """If a validator (or multiple validators) are defined for a particular setting key, run them against the 'value' field."""
        super().clean()

        # Encode as native values
        if self.is_int():
            self.value = self.as_int()

        elif self.is_bool():
            self.value = self.as_bool()

        validator = self.__class__.get_setting_validator(self.key, **kwargs)

        if validator is not None:
            self.run_validator(validator)

        options = self.valid_options()
        # print("############# clean Setting : "+ str(self.key)+" - value : "+str(self.value))
        if options and self.value not in options:
            raise ValidationError(_("Chosen value is not a valid option"))

    def run_validator(self, validator):
        """Run a validator against the 'value' field for this LabsManagerSetting object."""
        if validator is None:
            return

        value = self.value

        # Boolean validator
        if validator is bool:
            # Value must "look like" a boolean value
            if labsmanager.utils.is_bool(value):
                # Coerce into either "True" or "False"
                value = labsmanager.utils.str2bool(value)
            else:
                raise ValidationError({
                    'value': _('Value must be a boolean value')
                })

        # Integer validator
        if validator is int:

            try:
                # Coerce into an integer value
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError({
                    'value': _('Value must be an integer value'),
                })
        if isinstance(validator, DecimalValidator):
            try:
                # Coerce into an integer value
                value = Decimal(value)
            except (ValueError, TypeError):
                raise ValidationError({
                    'value': _('Value must be an Decimal value'),
                })
             
        # If a list of validators is supplied, iterate through each one
        if type(validator) in [list, tuple]:
            for v in validator:
                self.run_validator(v)

        if callable(validator):
            # We can accept function validators with a single argument

            if self.is_bool():
                value = self.as_bool()

            if self.is_int():
                value = self.as_int()

            validator(value)

    def validate_unique(self, exclude=None, **kwargs):
        """Ensure that the key:value pair is unique. In addition to the base validators, this ensures that the 'key' is unique, using a case-insensitive comparison.
        Note that sub-classes (UserSetting, PluginSetting) use other filters
        to determine if the setting is 'unique' or not
        """
        super().validate_unique(exclude)

        filters = {
            'key__iexact': self.key,
        }

        user = getattr(self, 'user', None)
        plugin = getattr(self, 'plugin', None)

        if user is not None:
            filters['user'] = user

        if plugin is not None:
            filters['plugin'] = plugin

        try:
            # Check if a duplicate setting already exists
            setting = self.__class__.objects.filter(**filters).exclude(id=self.id)

            if setting.exists():
                raise ValidationError({'key': _('Key string must be unique')})

        except self.DoesNotExist:
            pass

    def choices(self):
        """Return the available choices for this setting (or None if no choices are defined)."""
        return self.__class__.get_setting_choices(self.key, **self.get_kwargs())

    def valid_options(self):
        """Return a list of valid options for this setting."""
        choices = self.choices()

        if not choices:
            return None

        return [opt[0] for opt in choices]

    def is_choice(self):
        """Check if this setting is a "choice" field."""
        return self.__class__.get_setting_choices(self.key, **self.get_kwargs()) is not None

    def as_choice(self):
        """Render this setting as the "display" value of a choice field.
        E.g. if the choices are:
        [('A4', 'A4 paper'), ('A3', 'A3 paper')],
        and the value is 'A4',
        then display 'A4 paper'
        """
        choices = self.get_setting_choices(self.key, **self.get_kwargs())

        if not choices:
            return self.value

        for value, display in choices:
            if value == self.value:
                return display

        return self.value

    def is_model(self):
        """Check if this setting references a model instance in the database."""
        return self.model_name() is not None

    def model_name(self):
        """Return the model name associated with this setting."""
        setting = self.get_setting_definition(self.key, **self.get_kwargs())

        return setting.get('model', None)

    def model_class(self):
        """Return the model class associated with this setting.
        If (and only if):
        - It has a defined 'model' parameter
        - The 'model' parameter is of the form app.model
        - The 'model' parameter has matches a known app model
        """
        model_name = self.model_name()

        if not model_name:
            return None

        try:
            (app, mdl) = model_name.strip().split('.')
        except ValueError:
            # logger.error(f"Invalid 'model' parameter for setting {self.key} : '{model_name}'")
            return None

        app_models = apps.all_models.get(app, None)

        if app_models is None:
            # logger.error(f"Error retrieving model class '{model_name}' for setting '{self.key}' - no app named '{app}'")
            return None

        model = app_models.get(mdl, None)

        if model is None:
            # logger.error(f"Error retrieving model class '{model_name}' for setting '{self.key}' - no model named '{mdl}'")
            return None

        # Looks like we have found a model!
        return model

    def api_url(self):
        """Return the API url associated with the linked model, if provided, and valid!"""
        model_class = self.model_class()

        if model_class:
            # If a valid class has been found, see if it has registered an API URL
            try:
                return model_class.get_api_url()
            except Exception:
                pass

        return None

    def is_bool(self):
        """Check if this setting is required to be a boolean value."""
        validator = self.__class__.get_setting_validator(self.key, **self.get_kwargs())

        return self.__class__.validator_is_bool(validator)

    def as_bool(self):
        """Return the value of this setting converted to a boolean value.
        Warning: Only use on values where is_bool evaluates to true!
        """
        return labsmanager.utils.str2bool(self.value)

    def setting_type(self):
        """Return the field type identifier for this setting object."""
        if self.is_bool():
            return 'boolean'

        elif self.is_int():
            return 'integer'

        elif self.is_model():
            return 'related field'
        
        elif self.is_decimal():
            return 'decimal'

        else:
            return 'string'

    @classmethod
    def validator_is_bool(cls, validator):
        """Return if validator is for bool."""
        if validator == bool:
            return True

        if type(validator) in [list, tuple]:
            for v in validator:
                if v == bool:
                    return True

        return False

    def is_int(self,):
        """Check if the setting is required to be an integer value."""
        validator = self.__class__.get_setting_validator(self.key, **self.get_kwargs())

        return self.__class__.validator_is_int(validator)
    
    def is_decimal(self,):
        """Check if the setting is required to be an integer value."""
        validator = self.__class__.get_setting_validator(self.key, **self.get_kwargs())

        return self.__class__.validator_is_decimal(validator)

    @classmethod
    def validator_is_int(cls, validator):
        """Return if validator is for int."""
        if validator == int:
            return True

        if type(validator) in [list, tuple]:
            for v in validator:
                if v == int:
                    return True

        return False
    
    @classmethod
    def validator_is_decimal(cls, validator):
        """Return if validator is for int."""
        if  isinstance(validator, DecimalValidator):
            return True

        if type(validator) in [list, tuple]:
            for v in validator:
                if isinstance(v, DecimalValidator):
                    return True

        return False

    def as_int(self):
        """Return the value of this setting converted to a boolean value.
        If an error occurs, return the default value
        """
        try:
            value = int(self.value)
        except (ValueError, TypeError):
            value = self.default_value

        return value

    @classmethod
    def is_protected(cls, key, **kwargs):
        """Check if the setting value is protected."""
        setting = cls.get_setting_definition(key, **kwargs)

        return setting.get('protected', False)

    @property
    def protected(self):
        """Returns if setting is protected from rendering."""
        return self.__class__.is_protected(self.key, **self.get_kwargs())


def settings_group_options():
    """Build up group tuple for settings based on your choices."""
    return [('', _('No group')), *[(str(a.id), str(a)) for a in Group.objects.all()]]


def update_instance_url(setting):
    """Update the first site objects domain to url."""
    site_obj = Site.objects.all().order_by('id').first()
    site_obj.domain = setting.value
    site_obj.save()


def update_instance_name(setting):
    """Update the first site objects name to instance name."""
    site_obj = Site.objects.all().order_by('id').first()
    site_obj.name = setting.value
    site_obj.save()


def get_vac_zone():
    from leave.apiviews import get_vacation_zones_choices
    return get_vacation_zones_choices()
def get_default_vac_zone():
    from leave.apiviews import get_vacation_zones_choices
    return get_vacation_zones_choices()[0][0]

class LabsManagerSetting(BaseLabsManagerSetting):

    SETTINGS = {
         'MAIL_OBJECT_PREFIX': {
            'name': _('Mail Object Prefix'),
            'default': '[LabsManager]',
            'description': _('String added as prefix to mail object'),
            #'after_save': ,
        },
        'AUDIT_LOG_RETENTION': {
            'name': _('Audit Log Retention'),
            'description': _('Number of to retain AudiLog history'),
            'units': _('Days'),
            'default': 180,
            'validator': [
                int,
                MinValueValidator(1),
            ]
        },
        'VACATION_ZONE': {
            'name': _('French Vacation Zone'),
            'description': _('one of the zone defined for french vacation'),
            'default': 'Zone B',
            'choices': get_vac_zone,
            'type':'choices',
        },
         
    }       
        
    class Meta:
        verbose_name = "LabsManager Setting"
        verbose_name_plural = "LabsManager Settings"
        
    key = models.CharField(
        max_length=50,
        blank=False,
        unique=True,
        help_text=_('Settings key (must be unique - case insensitive'),
    )
    
    def to_native_value(self):
        """Return the "pythonic" value, e.g. convert "True" to True, and "1" to 1."""
        return self.__class__.get_setting(self.key)

def checkNotif(lmu):   
    print(f'object : {lmu} for user : {lmu.user}')
    from common.tasks import checkuser_notification_tasks 
    checkuser_notification_tasks(lmu.user)
    
class LMUserSetting(BaseLabsManagerSetting):
    
    SETTINGS = {
        'DASHBOARD_FUND_STALE_FROM_MONTH': {
            'name': _('Dashboard Stale From Calculation'),
            'description': _('Number of previous month to get in stale scope from now'),
            'default': 6,
            'validator': [int, MinValueValidator(1)]
        },
        'DASHBOARD_FUND_STALE_TO_MONTH': {
            'name': _('Dashboard Stale To Calculation'),
            'description': _('Number of month to get in stale scope from now'),
            'default': 0,
            'validator': [int, MinValueValidator(0)]
        },
        'DASHBOARD_CONTRACT_STALE_TO_MONTH': {
            'name': _('Contract Stale month'),
            'description': _('Number of month to get in stale scope from now'),
            'default': 3,
            'validator': [int, MinValueValidator(0)]
        },
        'DASHBOARD_PROJECT_STALE_TO_MONTH': {
            'name': _('Project Stale month'),
            'description': _('Number of month to get in stale scope from now'),
            'default': 3,
            'validator': [int, MinValueValidator(0)]
        },
        
        'DASHBOARD_MILESTONES_STALE_TO_MONTH': {
            'name': _('Milestones Stale to month'),
            'description': _('Number of month to get in stale scope from now'),
            'default': 3,
            'validator': [int, MinValueValidator(0)]
        },
        'DASHBOARD_MILESTONES_STALE_FROM_MONTH': {
            'name': _('Milestones Stale from month'),
            'description': _('Number of month to get in stale scope from now'),
            'default': 3,
            'validator': [int, MinValueValidator(0)]
        },
        
        'DASHBOARD_FUND_CONSOMATION_TYPE': {
            'name': _('Fund ratio consumption report type'),
            'description': _('Fund ratio consumption to report project in dahsboard'),
            'default': 'treshold',
            'choices': [
                ('treshold', 'treshold'),
                ('linear', 'linear Assumption'),
                ('both', 'both')
            ],
        },
        'DASHBOARD_FUND_CONSOMATION_RATIO': {
            'name': _('Fund ratio consumption threshold'),
            'description': _('Fund ratio consumption to report project in dahsboard'),
            'default': '0.1',
            'validator': [DecimalValidator(max_digits=2, decimal_places=2) ]
        },
        'DASHBOARD_FUND_CONSOMATION_USE_STALE_PERIOD': {
            'name': _('Use project Stale period for Consumption'),
            'description': _('use Project Stale month scope period for under consommation calculation'),
            'default': False,
            'validator': bool,
        },
        'DASHBOARD_FUND_CONSOMATION_LINEAR_RATIO_MARGIN': {
            'name': _('Margin to detect linear ratio'),
            'description': _('margin in % to identifyed deviation in budget consumption from linear ratio'),
            'default': '0.2',
            'validator': [DecimalValidator(max_digits=2, decimal_places=2) ],
        },
        'NOTIFCATION_STATUS': {
            'name': _('E-Mail Notification'),
            'description': _('enable automatic mail notification'),
            'default': True,
            'validator': bool,
            'after_save': checkNotif,
        },
        'NOTIFCATION_FREQ': {
            'name': _('Notification frequency'),
            'description': _('frequency wanted for notice transmission'),
            'default': '3 5 * * 5',
            'choices': [
                ('3 5 * * *', _('dayli')),
                ('3 5 * * 5', _('weekly')),
                ('3 5 1,15 * *', _('fortnightly')),
                ('3 5 1 * *', _('monthly'))
            ],
            'after_save': checkNotif,
        },
        'NOTIFCATION_INC_LEAVE': {
            'name': _('Notification Leaves'),
            'description': _('report all leaves of current month'),
            'default': False,
            'validator': bool,
        },
        'NOTIFCATION_LEAVE_FORMAT': {
            'name': _('Notification Leaves Format'),
            'description': _('choose to report by calendar or list view for leaves'),
            'default': 'calendar',
            'choices': [
                ('calendar', _('calendar')),
                ('list', _('list'))
            ],
        },
        'NOTIFCATION_LEAVE_REPORT_NONE': {
            'name': _('Notification Report Employee without leaves in calendar'),
            'description': _('report all employee even without leaves in calendar views'),
            'default': False,
            'validator': bool,
        },
        'NOTIFCATION_LEAVE_TIMEFRAME': {
            'name': _('Notification Leaves Timeframe'),
            'description': _('choose which timeframe to report (current month or 31 days timeframe)'),
            'default': '31days',
            'choices': [
                ('current', _('current month')),
                ('31days', _('31 days Timeframe'))
            ],
        },
        'NOTIFCATION_REPORT_LANGUAGE': {
            'name': _('Notification Report language'),
            'description': _('choose the language for reports'),
            'default': 'en',
            'choices':LANGUAGES,
        },
        'STICKY_NAVBAR': {
            'name': _('Fixed Navbar'),
            'description': _('navbar position fixed to the top of the screen'),
            'default': False,
            'validator': bool,
        },
        'PRINT_FULL_BOXES': {
            'name': _('Print Full Background colors'),
            'description': _('When printing, use displayed backgrounds instead of bordered boxew'),
            'default': True,
            'validator': bool,
        },
        'SHOW_PAST_ORG': {
            'name': _('Display Only Current Organisation'),
            'description': _('show/hide past hierarchical links'),
            'default': True,
            'validator': bool,
        },
        'LAB_THEME': {
            'name': _('Theme'),
            'description': _('Color theme for LabsManager'),
            'default': LabTheme.default_color_theme[0],
            'choices':LabTheme.get_themes_choices(),
        },
        
        
    }
    class Meta:
        """Meta options for LabsManagerUserSetting."""

        verbose_name = "LabsManager User Setting"
        verbose_name_plural = "LabsManager User Settings"
        constraints = [
            models.UniqueConstraint(fields=['key', 'user'], name='unique key and user')
        ]

    key = models.CharField(
        max_length=50,
        blank=False,
        unique=False,
        help_text=_('Settings key (must be unique - case insensitive)'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_('User'),
        help_text=_('User'),
    )

    def validate_unique(self, exclude=None, **kwargs):
        """Return if the setting (including key) is unique."""
        return super().validate_unique(exclude=exclude, user=self.user)

    def to_native_value(self):
        """Return the "pythonic" value, e.g. convert "True" to True, and "1" to 1."""
        return self.__class__.get_setting(self.key, user=self.user)

    def get_kwargs(self):
        """Explicit kwargs required to uniquely identify a particular setting object, in addition to the 'key' parameter."""
        return {
            'user': self.user,
        }
    
    