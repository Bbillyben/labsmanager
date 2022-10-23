from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from . import models
from .forms import FundItemModelForm, FundModelForm

    
################# FUND ITEM

class FundItemCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = FundItemModelForm
    success_message = 'Success: Fund Item was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    model = models.Fund_Item

    def get(self, request, *args, **kwargs):
        print(" FundItemCreateView "+str(kwargs))
        if 'pk' in kwargs:
            form = self.form_class(initial={'fund_item': kwargs['pk']})
        elif 'fund' in kwargs:
            form = self.form_class(initial={'fund': kwargs['fund']})
        else:
            form = self.form_class()        
        
        context = {'form': form}
        return render(request, self.template_name , context)

class FundItemUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Fund_Item
    template_name = 'form_validate_base.html'
    form_class = FundItemModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"

class FundItemDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Fund_Item
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('project_index')
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)
    
    
    
################# FUND

class FundCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = FundModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    model = models.Fund

    def get(self, request, *args, **kwargs):
        print("[ FundCreateView ] "+str(kwargs))
        if 'pk' in kwargs:
            form = self.form_class(initial={'fund': kwargs['pk']})
        elif 'project' in kwargs:
            form = self.form_class(initial={'project': kwargs['project']})
        else:
            form = self.form_class()        
        
        context = {'form': form}
        return render(request, self.template_name , context)

class FundUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Fund
    template_name = 'form_validate_base.html'
    form_class = FundModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"

class FundDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Fund
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('project_index')
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)