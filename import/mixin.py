from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str

from django.core.exceptions import PermissionDenied
from django.conf import settings

from import_export.forms import ConfirmImportForm, ImportExportFormBase
from import_export.signals import post_import
import import_export.admin

import warnings
class ImportViewMixin(import_export.admin.ImportMixin, generic.View):
        """
        Subclassing of ImportMixin as a generic View implementing ImportForm
        """
        #: template for import view
        import_template_name = 'import/import.html'
        #: resource class
        resource_class = None
        #: model to be imported
        model = None

        def get_confirm_import_form(self):
            '''
            Get the form type used to display the results and confirm the upload.
            '''
            return ConfirmImportForm

        def get(self, request, *args, **kwargs):
            """
            Overriding the GET part of ImportMixin.import_action method to be used without site_admin
            """
            return self.post(request, *args, **kwargs)

        def has_import_permission(self, request):
            if request.user.is_staff:
                return True
            if request.user.has_perm('common.import'):
                return True
            return False
        
        def post(self, request, *args, **kwargs):
            """
            Overriding the POST part of ImportMixin.import_action method to be used without site_admin
            """
            
            if not self.has_import_permission(request):
                raise PermissionDenied

            context = self.get_import_context_data()

            import_formats = self.get_import_formats()
            if getattr(self.get_form_kwargs, "is_original", False):
                # Use new API
                import_form = self.create_import_form(request)
            else:
                form_class = self.get_import_form_class(request)
                form_kwargs = self.get_form_kwargs(form_class, *args, **kwargs)

                if issubclass(form_class, ImportExportFormBase):
                    import_form = form_class(
                        import_formats,
                        request.POST or None,
                        request.FILES or None,
                        # resources=self.get_import_resource_classes(),
                        **form_kwargs,
                    )
                else:
                    warnings.warn(
                        "The ImportForm class must inherit from ImportExportFormBase, "
                        "this is needed for multiple resource classes to work properly. ",
                        category=DeprecationWarning,
                    )
                    import_form = form_class(
                        import_formats,
                        request.POST or None,
                        request.FILES or None,
                        **form_kwargs,
                    )

            resources = list()
            if request.POST and import_form.is_valid():
                input_format = import_formats[
                    int(import_form.cleaned_data["input_format"])
                ]()
                if not input_format.is_binary():
                    input_format.encoding = self.from_encoding
                import_file = import_form.cleaned_data["import_file"]

                if getattr(settings, "IMPORT_EXPORT_SKIP_ADMIN_CONFIRM", False):
                    data = bytes()
                    for chunk in import_file.chunks():
                        data += chunk
                    try:
                        dataset = input_format.create_dataset(data)
                    except Exception as e:
                        self.add_data_read_fail_error_to_form(import_form, e)
                    if not import_form.errors:
                        result = self.process_dataset(
                            dataset,
                            import_form,
                            request,
                            *args,
                            raise_errors=False,
                            rollback_on_validation_errors=True,
                            **kwargs,
                        )
                        if not result.has_errors() and not result.has_validation_errors():
                            return self.process_result(result, request)
                        else:
                            context["result"] = result
                else:
                    # first always write the uploaded file to disk as it may be a
                    # memory file or else based on settings upload handlers
                    tmp_storage = self.write_to_tmp_storage(import_file, input_format)
                    # allows get_confirm_form_initial() to include both the
                    # original and saved file names from form.cleaned_data
                    import_file.tmp_storage_name = tmp_storage.name

                    try:
                        # then read the file, using the proper format-specific mode
                        # warning, big files may exceed memory
                        data = tmp_storage.read()
                        dataset = input_format.create_dataset(data)
                    except Exception as e:
                        self.add_data_read_fail_error_to_form(import_form, e)

                    if not import_form.errors:
                        # prepare kwargs for import data, if needed
                        res_kwargs = self.get_import_resource_kwargs(
                            request, *args, form=import_form, **kwargs
                        )
                        resource = self.choose_import_resource_class(import_form)(
                            **res_kwargs
                        )
                        resources = [resource]

                        # prepare additional kwargs for import_data, if needed
                        imp_kwargs = self.get_import_data_kwargs(
                            request, *args, form=import_form, **kwargs
                        )
                        
                        result = resource.import_data(
                            dataset,
                            dry_run=True,
                            raise_errors=False,
                            file_name=import_file.name,
                            user=request.user,
                            **imp_kwargs,
                        )

                        context["result"] = result
                        if not result.has_errors() and not result.has_validation_errors():
                            if getattr(self.get_form_kwargs, "is_original", False):
                                # Use new API
                                context["confirm_form"] = self.create_confirm_form(
                                    request, import_form=import_form
                                )
                            else:
                                confirm_form_class = self.get_confirm_form_class(request)
                                initial = self.get_confirm_form_initial(
                                    request, import_form
                                )
                                context["confirm_form"] = confirm_form_class(
                                    initial=self.get_form_kwargs(
                                        form=import_form, **initial
                                    )
                                )
            else:
                res_kwargs = self.get_import_resource_kwargs(
                    request, *args, form=import_form, **kwargs
                )
                resource_classes = self.get_import_resource_classes()
                resources = [
                    resource_class(**res_kwargs) for resource_class in resource_classes
                ]


            context["title"] = _("Import")
            context["form"] = import_form
            context["opts"] = self.model._meta
            context["media"] = import_form.media
            context["fields_list"] = [
                (
                    resource.get_display_name(),
                    [f.column_name for f in resource.get_user_visible_fields()],
                )
                for resource in resources
            ]

            return TemplateResponse(request, [self.import_template_name], context)
            
class ConfirmImportViewMixin(import_export.admin.ImportMixin, generic.View):
        """
        Subclassing of ImportMixin as a generic View implementing ConfirmImportForm
        """
        #: template for import view
        import_template_name = 'import/import.html'
        import_out_template= 'import/import_out.html'
        #: resource class
        resource_class = None
        #: model to be imported
        model = None

        def get_confirm_import_form(self):
            '''
            Get the form type used to display the results and confirm the upload.
            '''
            return ConfirmImportForm

        def post(self, request, *args, **kwargs):
            """
            Perform the actual import action (after the user has confirmed the import)
            """

            if not self.has_import_permission(request):
                raise PermissionDenied

            if getattr(self.get_confirm_import_form, "is_original", False):
                confirm_form = self.create_confirm_form(request)
            else:
                form_type = self.get_confirm_import_form()
                confirm_form = form_type(request.POST)

            if confirm_form.is_valid():
                import_formats = self.get_import_formats()
                input_format = import_formats[
                    int(confirm_form.cleaned_data["input_format"])
                ](encoding=self.from_encoding)
                encoding = None if input_format.is_binary() else self.from_encoding
                tmp_storage_cls = self.get_tmp_storage_class()
                tmp_storage = tmp_storage_cls(
                    name=confirm_form.cleaned_data["import_file_name"],
                    encoding=encoding,
                    read_mode=input_format.get_read_mode(),
                )

                data = tmp_storage.read()
                dataset = input_format.create_dataset(data)
                result = self.process_dataset(
                    dataset, confirm_form, request, *args, **kwargs
                )

                tmp_storage.remove()

                return self.process_result(result, request)
            
        def process_result(self, result, request):
            self.generate_log_entries(result, request)
            self.add_success_message(result, request)
            post_import.send(sender=None, model=self.model)
            
            context={
                'result':result,
            }
            return TemplateResponse(request, self.import_out_template, context)