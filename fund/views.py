from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from view_breadcrumbs import BaseBreadcrumbMixin
from .models import Fund, Fund_Item
from expense.models import Expense_point, Cost_Type
from django.db.models import Value, Count
import pandas as pd
import json

def get_fundItem_table(request, pk):
    fundP=Fund.objects.filter(pk=pk).first()
    data = {'fund': fundP}  
    print ("================ >>> "+str(fundP))  
    return render(request, 'fund/fund_item_table.html', data)


def get_fund_global_overview(request, pk):
        print("--------------------> "+pk)
        a=Fund_Item.objects.values_list('type__name', 'amount', named=False).filter(fund=pk).annotate(source=Value('Fund'))

        # get cost type
        cts=Cost_Type.objects.all()
        bp = Expense_point.objects.none()
        EPa=Expense_point.objects.filter(fund=pk).annotate(source=Value('Expense'))
        for ct in cts:
            bpT=EPa.filter(type=ct.pk).order_by('-value_date').first()
            if bpT:
                bp= bp.union(EPa.filter(pk=bpT.pk))
        
        b=bp.values_list('type__name', 'amount', 'source', named=False)
        c = a.union(b)
        cpd=pd.DataFrame.from_records(c, columns=["type","amount","source"])
        piv=cpd.pivot_table(index="type", columns="source", values="amount", aggfunc='sum', margins=True, margins_name='Sum')
    
        data = {'df': piv, 'title':'overview', 'table_id':'fund_overview_table'}  
        
        return render(request, 'pandas/basic_table.html', data)