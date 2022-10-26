from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from view_breadcrumbs import BaseBreadcrumbMixin
from .models import Contract, Contract_expense


class ContractIndexView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'expense/contract_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Contract
    crumbs = [("Contracts","contracts")]
    
    
# Create your views here.

def get_contractExpense_table(request, pk):
    cont=Contract.objects.filter(pk=pk).first()
    data = {'contract': cont}   
    return render(request, 'expense/contract_item_expense.html', data)