from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from . import models
from .forms import LeaveItemModelForm

class LeaveItemCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = LeaveItemModelForm
    success_message = 'Success: Fund Item was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    model = models.Leave

    def get(self, request, *args, **kwargs):
        print("LeaveItemCreateView - GET")
        print("  - args :"+str(args))
        print("  - kwargs :"+str(kwargs))
        
        
        initial={}
        
        data=request.GET # or request.data or request.query_params
        
        if 'emp_pk' in kwargs:
            initial['employee']=kwargs['emp_pk']
            
        
        start_date=data.get("start_date", None)
        if start_date is not None:
            start_date=start_date.split("T")[0]
            initial['start_date']=start_date
        
        end_date=data.get("end_date", None)
        if end_date is not None:
            end_date=end_date.split("T")[0]
            initial['end_date']=end_date
        
        print("  - initial : "+str(initial))
        
        form = self.form_class(initial=initial)
        context = {'form': form}
        return render(request, self.template_name , context)
    
    
class LeaveItemUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Leave
    template_name = 'form_validate_base.html'
    form_class = LeaveItemModelForm
    success_message = 'Success: Leave was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    
class LeaveItemDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Leave
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('project_index')
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)