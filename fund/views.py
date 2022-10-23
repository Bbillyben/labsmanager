from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from view_breadcrumbs import BaseBreadcrumbMixin
from .models import Fund, Fund_Item

def get_fundItem_table(request, pk):
    fundP=Fund.objects.filter(pk=pk).first()
    data = {'fund': fundP}  
    print ("================ >>> "+str(fundP))  
    return render(request, 'fund/fund_item_table.html', data)