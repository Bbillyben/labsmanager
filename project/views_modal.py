from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from . import models
from .forms import ProjectModelForm, ParticipantModelForm


# Update
class ProjectUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Project
    template_name = 'form_validate_base.html'
    form_class = ProjectModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    
class ProjectCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = ProjectModelForm
    success_message = 'Success: Employee was created.'
    success_url = reverse_lazy('project_index')
    
# remove
class ProjectRemoveView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Project
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('employee_index')




#### Participant
class ParticipantUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Participant
    template_name = 'form_validate_base.html'
    form_class = ParticipantModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"

# remove
class ParticipantDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Participant
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('employee')
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)
    
class ParticipantCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = ParticipantModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    model = models.Participant

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            form = self.form_class(initial={'project': kwargs['pk']})
        elif 'employee' in kwargs:
            form = self.form_class(initial={'employee': kwargs['employee']})
        else:
            form = self.form_class()
        
        context = {'form': form}
        return render(request, self.template_name , context)