from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.dateformat import format
import time

from django.db.models import Q

from django.views.generic.base import View
from rest_framework.decorators import action

from django.utils.functional import cached_property
from django.urls import reverse, reverse_lazy
from view_breadcrumbs import BaseBreadcrumbMixin

from settings.models import LMUserSetting


from project.models import Project
from fund.models import Fund_Item, Fund
from dashboard import utils

class DashboardView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    """View for index page."""
    template_name = 'dashboard/global_dashboard.html' #'labmanager/index.html
    crumbs = [("Dashboard","dashboard")]
    
class FundLossView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('Loss Project Main not yet defined!')


class FundLossCardView(LoginRequiredMixin, BaseBreadcrumbMixin, View):  
    
    template_general="dashboard/dasboard_loss_card.html" 
    
    def get(self, request, *args, **kwargs):
        import pandas as pd
        
        q_objects = Q(is_active=True) & Q(project__status=True) # base Q objkect
        slot = utils.getDashboardTimeSlot(request)
        if 'from' in slot:
            q_objects = q_objects & Q(end_date__gte=slot["from"])
        if 'to' in slot:
            q_objects = q_objects & Q(end_date__lte=slot["to"])
            
        fund=Fund.objects.filter(q_objects).order_by('end_date')
        if not fund:
            context={'data':{},
                 'type':'line',
                 'title':_("Project Loss Overview"),
                 }  
            return render(request, self.template_general, )
        frames=[]
        for fu in fund:
            avail=fu.get_available()
            frames.append(avail)
            
        result = pd.concat(frames)
        result= result.groupby(['project', 'funder','institution', 'type','end_date',]).sum().sort_values(by='end_date')
        dataTosend=result.to_json(orient='table')
        
        context={'data':dataTosend,
                 'type':'line',
                 'title':_("Project Loss Overview"),
                 'action':[
                        {'name':"", 'url':reverse('project_index'), 'icon':'fa-eye'}
                    ]  
                 }  
        return render(request, self.template_general, context)
    
class fundStaleView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(str(self.__class__.__name__)+' Main not yet defined!')
    
class fundStaleCardView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    template_general="dashboard/dashboard_table.html"
    
    def get(self, request, *args, **kwargs):
        
        context={
            'url':reverse_lazy("api:fund-stale_fund"),
            'title':_('Stale Fund'),
            'columns':[
                {'name':_('project'),'item':'project',  'formatter':'ProjectFormatter'},
                {'name':_('funder'),'item':'funder'},
                {'name':_('Institution'),'item':'institution'},
                {'name':_('end date'),'item':'end_date', 'formatter':'dueDatePassed'},
                {'name':_('Availability'),'item':'availability', 'formatter':'moneyFormatter'},
            ], 
            'action':[
                {'name':"", 'url':reverse('project_index'), 'icon':'fa-eye'}
            ]        
        }
        
        return render(request, self.template_general, context)


class contractstaleView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(str(self.__class__.__name__)+' Main not yet defined!')
    
class contractstaleCardView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    template_general="dashboard/dashboard_table.html"
    
    def get(self, request, *args, **kwargs):
        
        context={
            'url':reverse_lazy("api:contract-contract_stale"),
            'title':_('Stale Contract'),
            'columns':[
                {'name':_('Employee'),'item':'employee',  'formatter':'employeeFormatter'},
                {'name':_('Project'),'item':'fund.project', 'formatter':'ProjectFormatter'},
                {'name':_('Institution'),'item':'fund.institution.short_name'},
                {'name':_('Contract Type'),'item':'contract_type'},
                {'name':_('end date'),'item':'end_date', 'formatter':'dueDatePassed'},
                
            ], 
            'action':[
                {'name':"", 'url':reverse('contract_index'), 'icon':'fa-eye'}
            ]        
        }
        
        return render(request, self.template_general, context)
