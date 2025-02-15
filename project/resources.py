from django.utils.translation import gettext as _
from django.db.models import Q
from labsmanager.ressources import labResource, InfoWidget
from .models import Project, Participant, Institution_Participant
from fund.models import Fund
from import_export.fields import Field
from labsmanager.utils import getDateFilter
import import_export.widgets as widgets
from import_export.fields import Field

class LeadertWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        pa=Participant.objects.filter(project=value, status="l")
        
        li=[]
        for c in pa:
            strC= str(c.employee.user_name) 
            strC+= " - " +str(c.get_status_display())
            strC+= " (" +str(c.start_date)
            strC+= " > " +str(c.end_date)+')'
            strC+= '#'+str(c.quotity)
            li.append(strC)
           
        return "\n".join(li)
    
class ParticipantWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        pa=Participant.objects.filter(Q(project=value) & ~Q(status="l"))
        
        li=[]
        for c in pa:
            strC= str(c.employee.user_name) 
            strC+= " - " +str(c.get_status_display())
            strC+= " (" +str(c.start_date)
            strC+= " > " +str(c.end_date)+')'
            strC+= '#'+str(c.quotity)
            li.append(strC)
           
        return "\n".join(li)

class InstitutionWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        pa=Institution_Participant.objects.filter(project=value)
        
        li=[]
        for c in pa:
            strC= str(c.institution.short_name) 
            strC+= " - " +str(c.get_status_display())
            li.append(strC)    
        return "\n".join(li)    
    
class FundWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        pa=Fund.objects.filter(project=value)
        
        li=[]
        for c in pa:
            strC= str(c.funder.short_name) 
            strC+= " - " +str(c.institution.short_name)
            strC+='('+str(c.ref)
            strC+=' - '+str(c.amount)+")"
            li.append(strC)    
        return "\n".join(li)    
    
       
class ProjectResource(labResource):
    leader = Field(
        column_name=_('Leader'),
        attribute='pk', 
        widget=LeadertWidget(), readonly=True
        )
    participants = Field(
        column_name=_('participant'),
        attribute='pk', 
        widget=ParticipantWidget(), readonly=True
        )
    institution = Field(
        column_name=_('Institution'),
        attribute='pk', 
        widget=InstitutionWidget(), readonly=True
        )
    Fund = Field(
        column_name=_('Fund'),
        attribute='pk', 
        widget=FundWidget(), readonly=True
        )
    Total_fund=Field(
        column_name=_('Total Fund'),
        attribute='get_funds_amount', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    Total_expense=Field(
        column_name=_('Total Expense'),
        attribute='get_funds_expense', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    Total_Available=Field(
        column_name=_('Total Available'),
        attribute='get_funds_available', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    Total_fund_focus=Field(
        column_name=_('Total Fund Focus'),
        attribute='get_funds_amount_f', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    Total_expense_focus=Field(
        column_name=_('Total Expense Focus'),
        attribute='get_funds_expense_f', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    Total_Available_focus=Field(
        column_name=_('Total Available Focus'),
        attribute='get_funds_available_f', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    info=Field(
        column_name=_('Infos'),
        attribute='info', 
        widget=InfoWidget(), 
        readonly=True
    )
    class Meta:
        """Metaclass"""
        model = Project
        skip_unchanged = False
        clean_model_instances = False
        exclude = [ 'id',
         ]
        export_order=['name',
                      'start_date',
                      'end_date',
                      'institution',
                      'leader',
                      'participants',
                      'Fund',
                      'Total_fund',
                      'Total_expense',
                      'Total_Available',
                      'Total_fund_focus',
                      'Total_expense_focus',
                      'Total_Available_focus',
                      ]