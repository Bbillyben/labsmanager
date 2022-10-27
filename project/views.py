from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from view_breadcrumbs import BaseBreadcrumbMixin
from fund.models import Fund, Fund_Item, Cost_Type
from expense.models import Expense_point
from django.db.models import Value, Count
import pandas as pd
import json

class ProjectIndexView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'project/project_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Project
    crumbs = [("Project","project")]
    
    
    
class ProjectView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'project/project_single.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Project
    # crumbs = [("Project","project")]
    
    @cached_property
    def crumbs(self):
        return [("Project","./",) ,
                (str(self.construct_crumb()) ,  reverse("project_single", kwargs={'pk':'4'} ) ),
                ]

    def construct_crumb(self):
        proj = Project.objects.get(pk=self.kwargs['pk'])
        return proj
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the Employee view:
            - employee : the employee corresponding
        """
        context = super().get_context_data(**kwargs).copy()

        if not 'pk' in kwargs:
            return context

        id=kwargs.get("pk", None)
        proj = Project.objects.filter(pk=id)
        context['project'] = proj.first()

        # View top-level categories
        return context


def get_project_resume(request, pk):
    proj = Project.objects.filter(pk=pk).first()
    data = {'project': proj}
    
    return render(request, 'project/project_desc_table.html', data)

def get_project_fund_overview(request, pk):
    fund=Fund.objects.filter(project=pk).values("pk")
    a=Fund_Item.objects.values_list('fund__ref', 'type__name', 'amount', named=False).filter(fund__in=fund).annotate(source=Value('Fund'))
    
     # get cost type
    cts=Cost_Type.objects.all()
    bp = Expense_point.objects.none()
    EPa=Expense_point.objects.filter(fund__in=fund).annotate(source=Value('Expense'))
    for ct in cts:
        bpT=EPa.filter(type=ct.pk).order_by('-value_date').first()
        if bpT:
            bp= bp.union(EPa.filter(pk=bpT.pk))
    
    b=bp.values_list('fund__ref', 'type__name', 'amount', 'source', named=False)
    c = a.union(b)
    cpd=pd.DataFrame.from_records(c, columns=['fund', "type","amount","source"])
    piv=cpd.pivot_table(index="type", columns=["fund","source"], values="amount", aggfunc='sum', margins=True, margins_name='Sum',fill_value="-")

    data = {'df': piv, 'title':'overview', 'table_id':'project_overview_table'}  
    # jsonD = piv.reset_index().to_json(orient='records')
    # vals=json.loads(jsonD)
    #return render(request, 'pandas/basic_table.html', data)
    # return JsonResponse(vals, safe=False)
    return HttpResponse(piv.to_html())
    
    