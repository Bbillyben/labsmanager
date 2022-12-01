from django.utils.translation import gettext as _
from django.db.models import Q
from labsmanager.ressources import labResource
from .models import Fund_Item, Fund, Cost_Type
from import_export.fields import Field
from labsmanager.utils import getDateFilter
import import_export.widgets as widgets
from import_export.fields import Field


        
        
class FundItemResource(labResource):
    available=Field(
        column_name=_('Total Available'),
        attribute='available', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    type=Field(
        column_name=_('type'),
        attribute='type', 
        widget=widgets.ForeignKeyWidget(Cost_Type, 'name'), readonly=True
    )
    project=Field(
        column_name=_('Project'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'project__name'), readonly=True
    )
    funder=Field(
        column_name=_('funder'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'funder__short_name'), readonly=True
    )
    institution=Field(
        column_name=_('institution'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'institution__short_name'), readonly=True
    )
    start_date=Field(
        column_name=_('Start Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'start_date'), readonly=True
    )
    end_date=Field(
        column_name=_('End Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'end_date'), readonly=True
    )
    ref=Field(
        column_name=_('Red'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'ref'), readonly=True
    )
    
    class Meta:
        """Metaclass"""
        model = Fund_Item
        skip_unchanged = False
        clean_model_instances = False
        exclude = [ 'id','fund' ]
        export_order=['project', 
                      'funder',
                      'institution',
                      'start_date',
                      'end_date',
                      'type',
                      'ref',
                      'amount',
                      'expense',
                      'available',
                      ]