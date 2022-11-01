from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django.views.generic.base import View
from rest_framework.decorators import action

from django.utils.functional import cached_property
from django.urls import reverse, reverse_lazy
from view_breadcrumbs import BaseBreadcrumbMixin



from project.models import Project
from fund.models import Fund_Item, Fund

class FundLossView(LoginRequiredMixin, BaseBreadcrumbMixin, View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('Loss Project Main not yet defined!')


class FundLossCardView(LoginRequiredMixin, BaseBreadcrumbMixin, View):  
    
    template_general="dashboard/dasboard_simple.html" 
    
    def get(self, request, *args, **kwargs):
        
        fund=Fund.objects.filter(Q(is_active=True)).order_by('end_date')
        
        pDic={'labels':[],
              'project':[],
              'values':[],
        }
        prev=0
        for fu in fund:
            avail=fu.get_available()
            sumA=abs(avail['amount'].sum(axis=0, skipna=True))
            
            if not (fu.end_date) in pDic['labels']:
                pDic['labels'].append((fu.end_date))
                pDic['project'].append(fu.project.name)
                pDic['values'].append(sumA+prev)
            else:
                id=pDic['labels'].index((fu.end_date))
                pDic['values'][id]+=sumA
                if not fu.project.name in pDic['project'][id] :
                    pDic['project'][id]+=', '+ fu.project.name
            prev=pDic['values'][-1]
            #print(' fu :'+str(fu.project.name)+" / "+str(fu.end_date)+" : "+str(sumA))
        context={'data':pDic,
                 'type':'line',
                 'title':_("Project Loss Overview"),
                 'action':[
                        {'name':"", 'url':reverse('project_index'), 'icon':'fa-eye'}
                    ]  
                 }  
        # return JsonResponse(context, safe=False)  
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
