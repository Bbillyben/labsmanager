from django.db import models
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.template import Context, Template
from django.http import HttpResponse, JsonResponse
from django.contrib.contenttypes.models import ContentType  
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _


import datetime
import logging
import os
import sys


from io import BytesIO
from django.http import FileResponse, JsonResponse
from docxtpl import DocxTemplate
from django_weasyprint import WeasyTemplateResponseMixin
import jinja2
import json

from django.urls import reverse
from django.utils.html import format_html

from staff.models import Employee,Employee_Status, GenericInfo, Team, TeamMate, Employee_Superior
from expense.models import Contract
from project.models import Project, Participant, Institution_Participant
from project.views import get_project_fund_overview
from leave.models import Leave
from fund.models import Budget, Fund, Fund_Item, Contribution
from endpoints.models import Milestones
from project.views import get_project_fund_overviewReport
from infos.models import GenericNote  

from . import serializers
from labsmanager.helpers import DownloadFile
from labsmanager import settings
from labsmanager.manager import FileModelManager
from .signals import auto_delete_templatefile_on_delete
logger = logging.getLogger("labsmanager")

from plugin import registry


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
        logger.debug(f'BaseReport - rename_file to "{fullpath}"')

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

        template = template.replace('/', os.path.sep)
        template = template.replace('\\', os.path.sep)

        template = settings.MEDIA_ROOT.joinpath(template)
        logger.debug(f'BaseReport - template_name to "{template}"')
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

class TemplateReport(BaseReport):  
    objects = FileModelManager()
    
    class Meta:
        abstract = True
        
    @classmethod
    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)
        models.signals.post_delete.connect(auto_delete_templatefile_on_delete, sender=cls)
    
    def get_context_data(self, request, options):
        """Supply context data to the template for rendering."""
        context = {}
        context['request']= request
        context['options']= options
        context['template']= self
        context["current_date"]=datetime.datetime.now()
        return context
    
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
        raise  Exception("render method as to be overriden in TemplateReport")
    
    def download_link(self):
        app_label = self._meta.app_label
        model_name = self._meta.model_name
        if self.template:
            url = reverse('download_template_report', args=[app_label, model_name, self.pk])
            return format_html('<a href="{}" target="_blank">%s</a>'%self.template.name, url)
        return  _("No file")
    
    download_link.short_description = _("Template Report Link")
    
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
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx','html'])],
    )
    
class WordReport(TemplateReport):   
    class Meta:
        abstract = True
    
    
    def render(self, request, options):
        options["rendering"]="word"
        # rendering    
        doc = DocxTemplate(self.template_name)
        jinja_env = jinja2.Environment(autoescape=False)
        doc.render( self.get_context(request, options), autoescape=True)
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        
        filename = self.generate_filename(request, options)
        logger.debug(f'>>>  WordReport - Render :')
        logger.debug(f'    - filename : {filename}')
        logger.debug(f'    - template : {self.template.path}')
        response = DownloadFile(doc_io.read(), 
                                filename, 
                                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                )
        return response

from django_weasyprint import WeasyTemplateResponseMixin
class WeasyprintReportMixin(WeasyTemplateResponseMixin):
    """Class for rendering a HTML template to a PDF."""

    pdf_filename = 'report.pdf'
    pdf_attachment = True

    def __init__(self, request, template, **kwargs):
        """Initialize the report mixin with some standard attributes"""
        self.request = request
        self.template_name = template
        self.pdf_filename = kwargs.get('filename', 'report.pdf')
        
class PdfReport(TemplateReport):
    class Meta:
        abstract = True
        
    def render(self, request, options, **kwargs):  
        options["rendering"]="pdf"    
        wp = WeasyprintReportMixin(
            request,
            self.template_name,
            base_url=request.build_absolute_uri("/"),
            presentational_hints=True,
            filename=self.generate_filename(request, options)
        )
        context = self.get_context(request, options)
        return wp.render_to_response(context, **kwargs)
    
class EmployeeReport(TemplateReport):   
    class Meta:
        abstract = True
           
    def get_context_data(self, request, options):              
        pk=options.get('pk', None)
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        slot={}
        if start_date:
            slot['from']=start_date
        if end_date:
            slot['to']=end_date
            
        if not pk:
            return {}
        context=super().get_context_data(request, options)
        

        emp = Employee.objects.get(pk=pk)
        if not emp:
            return HttpResponse("not found", code=404)
        context["employee"]=emp
        
        info = GenericInfo.objects.filter(employee__pk=pk)
        context["info"]=info
        status = Employee_Status.objects.filter(employee__pk=pk).order_by('start_date')
        context["status"]=status
        
        contract = Contract.effective.filter(employee__pk=pk).order_by('start_date')
        context["contract"]=contract
        
        contract_provisionnal = Contract.provisionnal.filter(employee__pk=pk).order_by('start_date')
        context["contract_prov"]=contract_provisionnal
        
        partProj = Participant.objects.filter(employee=emp).order_by('start_date')
        context["project"]=partProj
        
        leave = Leave.objects.timeframe(slot).filter(employee=emp).order_by('-start_date')
        context["leave"]=leave
        
        context["Contribution"] = Contribution.objects.filter(employee=emp).order_by('start_date')
        
        tm = TeamMate.objects.filter(employee=emp).values("team")
        teams = Team.objects.filter(models.Q(leader=emp) | models.Q(pk__in=tm))
        context["teams"]=teams
        
        superior = Employee_Superior.objects.filter(employee = emp)
        context["superior"]=superior
        
        subordinate = Employee_Superior.objects.filter(superior = emp)
        context["subordinate"]=subordinate
        
        employee_content_type = ContentType.objects.get_for_model(Employee)
        notes = GenericNote.objects.filter(content_type=employee_content_type,object_id=emp.id)
 
        context["notes"]=notes
        
        # for plugin
        for plugin in registry.with_mixin('report'):
            try:
                plugin.add_report_data(self, request, context)
            except Exception as e:
                logger.error(
                    f'plugins.{plugin.slug}.add_report_context on {self} raise error :{e}'
                )
        return context 
    
    
class EmployeeWordReport(EmployeeReport, WordReport):
    @classmethod
    def getSubdir(cls):
        return 'employee'
 
class EmployeePDFReport(EmployeeReport, PdfReport):
    @classmethod
    def getSubdir(cls):
        return 'employee'
    
from project.views import get_project_fund_overviewReport_bytType
from project.models import GenericInfoProject
from expense.models import Expense
class ProjectReport(TemplateReport):
    class Meta:
        abstract = True
    
    def get_context_data(self, request, options):
        pk=options.get('pk', None)
        if not pk:
            return {}
        context=super().get_context_data(request, options)
        
        proj = Project.objects.get(pk=pk)
        if not proj:
            return HttpResponse("not found", code=404)
        context["project"]=proj
        
        info = GenericInfoProject.objects.filter(project__pk=pk)
        context["info"]=info
        
        context["institution"] = Institution_Participant.objects.filter(project=pk)
        
        context["participant"] = Participant.objects.filter(project=pk)
        
        context["contract"] = Contract.effective.filter(fund__project=pk)
        
        context["budget"] = Budget.objects.filter(fund__project=pk)
        
        context["Contribution"] = Contribution.objects.filter(fund__project=pk)
        
        context["milestone"] = Milestones.objects.filter(project=pk)
        
        
        # generating from html template for fund overview        
        # context["fundoverview"]=get_project_fund_overviewReport(pk)
        
        # Fund and related items
        fi = Fund.objects.filter(project=pk)
        # d=json.dumps(serializers.FundProjectReportSerializer(fi, many=True).data, cls=DjangoJSONEncoder)
        d=json.loads(json.dumps(serializers.FundProjectReportSerializer(fi, many=True).data, cls=DjangoJSONEncoder))
        context["fund"]=d
        
        # fund overvieww by type
        fuT = get_project_fund_overviewReport_bytType(pk)
        context["fund_overview"]=fuT
        
        
        # expense :
        exp = Expense.object_inherit.filter(fund_item__in=fi).select_subclasses().order_by('-date')
        expS = {}
        for e in exp:
            idF=e.fund_item.pk
            if not idF in expS:
                expS[idF]= []
            expS[idF].append(e)
        context["expense"] = expS
        # fore Generic Notes
        ct = ContentType.objects.get_for_model(Project)
        notes = GenericNote.objects.filter(content_type=ct,object_id=proj.id)
 
        context["notes"]=notes
        
        # for plugin
        for plugin in registry.with_mixin('report'):
            try:
                plugin.add_report_data(self, request, context)
            except Exception as e:
                logger.error(
                    f'plugins.{plugin.slug}.add_report_context on {self} raise error :{e}'
                )
        
        return context 

class ProjectWordReport(ProjectReport, WordReport):
    
    @classmethod
    def getSubdir(cls):
        return 'project'
    
class ProjectPDFReport(ProjectReport, PdfReport):
    
    @classmethod
    def getSubdir(cls):
        return 'project'