from django.db import models
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.template import Context, Template
from django.http import HttpResponse


from django.utils.translation import gettext_lazy as _


import datetime
import logging
import os
import sys


from io import BytesIO
from django.http import FileResponse
from docxtpl import DocxTemplate
import jinja2

from staff.models import Employee,Employee_Status, GenericInfo
from expense.models import Contract
from project.models import Project, Participant
from leave.models import Leave



from labsmanager import settings



logger = logging.getLogger("labsmanager")



def rename_template(instance, filename):
    """Helper function for 'renaming' uploaded report files.
    Pass responsibility back to the calling class,
    to ensure that files are uploaded to the correct directory.
    """
    return instance.rename_file(filename)


# Create your models here.

class BaseReport(models.Model):
    class Meta:
        abstract = True
        

    def save(self, *args, **kwargs):
        self.revision += 1
        super().save()
    
    def __str__(self):
        return "{n} - {d}".format(n=self.name, d=self.description)
    
    @property
    def extension(self):
        """Return the filename extension of the associated template file"""
        return os.path.splitext(self.template.name)[1].lower()
    
    @classmethod
    def getSubdir(cls):
        """Return the subdirectory where template files for this report model will be located."""
        return ''
    
    def rename_file(self, filename):
        """Function for renaming uploaded file"""

        filename = os.path.basename(filename)

        path = os.path.join('report', 'report_template', self.getSubdir(), filename)

        fullpath = settings.MEDIA_ROOT.joinpath(path).resolve()

        # If the report file is the *same* filename as the one being uploaded,
        # remove the original one from the media directory
        if str(filename) == str(self.template):

            if fullpath.exists():
                logger.info(f"Deleting existing report template: '{filename}'")
                os.remove(fullpath)

        # Ensure that the cache is cleared for this template!
        cache.delete(fullpath)

        return path
    
    @property
    def template_name(self):
        """Returns the file system path to the template file.
        Required for passing the file to an external process
        """
        template = self.template.name

        # TODO @matmair change to using new file objects
        template = template.replace('/', os.path.sep)
        template = template.replace('\\', os.path.sep)

        template = settings.MEDIA_ROOT.joinpath(template)

        return template
    
    name = models.CharField(
        blank=False, max_length=100,
        verbose_name=_('Name'),
        help_text=_('Template name'),
    )
    
    template = models.FileField(
        upload_to=rename_template,
        verbose_name=_('Template'),
        help_text=_("Report template file"),
        # validators=[FileExtensionValidator(allowed_extensions=['html', 'htm', 'doc', 'docx',])],
    )
    
    description = models.CharField(
        max_length=250,
        verbose_name=_('Description'),
        help_text=_("Report template description")
    )
    
    revision = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Revision"),
        help_text=_("Report revision number (auto-increments)"),
        editable=False,
    )
    
class WordReport(BaseReport):
    class Meta:
        abstract = True
    
    def get_context_data(self, request, options):
        """Supply context data to the template for rendering."""
        return {}
    
    def get_context(self, request, options):
        """All context to be passed to the renderer."""
        # Generate custom context data based on the particular report subclass
        context = self.get_context_data(request, options)

        context['date'] = datetime.datetime.now().date()
        context['datetime'] = datetime.datetime.now()
        context['datetime_SI'] = datetime.datetime.now().strftime("%Y_%m_%d")
        context['report_description'] = self.description
        context['report_name'] = self.name
        context['report_revision'] = self.revision
        context['request'] = request
        context['user'] = request.user

        return context
    
    def generate_filename(self, request, options):
        """Generate a filename for this report."""
        template_string = Template(self.filename_pattern)

        ctx = self.get_context(request, options)

        context = Context(ctx)

        return template_string.render(context)
    
    def render(self, request, options):
        # rendering    
        doc = DocxTemplate(self.template_name)
        jinja_env = jinja2.Environment(autoescape=True)
        doc.render( self.get_context(request, options), autoescape=True)
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        response = HttpResponse(doc_io.read())
        filename = self.generate_filename(request, options)
        response["Content-Disposition"] = "attachment; filename="+filename

        # Set the appropriate Content-Type for docx file
        response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        return response
    
    filename_pattern = models.CharField(
        default="report.docx",
        verbose_name=_('Filename Pattern'),
        help_text=_('Pattern for generating report filenames'),
        max_length=100,
    )

    enabled = models.BooleanField(
        default=True,
        verbose_name=_('Enabled'),
        help_text=_('Report template is enabled'),
    )
    template = models.FileField(
        upload_to=rename_template,
        verbose_name=_('Template'),
        help_text=_("Report template file"),
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx',])],
    )
    
    
class EmployeeWordReport(WordReport):
    @classmethod
    def getSubdir(cls):
        return 'employee'
    
    def get_context_data(self, request, options):
        pk=options.get('pk', None)
        if not pk:
            return {}
        context={'request': request,}
        
        
        emp = Employee.objects.get(pk=pk)
        if not emp:
            return HttpResponse("not found", code=404)
        context["employee"]=emp
        
        info = GenericInfo.objects.filter(employee__pk=pk)
        context["info"]=info
        status = Employee_Status.objects.filter(employee__pk=pk)
        context["status"]=status
        
        contract = Contract.objects.filter(employee__pk=pk)
        context["contract"]=contract
        
        partProj = Participant.objects.filter(employee=emp)
        # project = Project.objects.filter(pk__in=partProj)
        context["project"]=partProj
        
        leave = Leave.objects.filter(employee=emp)
        # project = Project.objects.filter(pk__in=partProj)
        context["leave"]=leave
        
        return context
        