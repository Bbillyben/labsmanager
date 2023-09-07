from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from . import models
from .forms import ProjectModelForm, ParticipantModelForm, InstitutionModelForm, InstitutionModelFormDirect, GenericInfoProjectForm, GenericInfoTypeProjectForm

from labsmanager.mixin import CreateModalNavigateMixin
# Update
class ProjectUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Project
    template_name = 'form_validate_base.html'
    form_class = ProjectModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    
class ProjectCreateView(LoginRequiredMixin, CreateModalNavigateMixin):
    template_name = 'form_base.html'
    form_class = ProjectModelForm
    success_message = 'Success: Employee was created.'
    success_url = reverse_lazy('project_index')
    
    success_single = 'project_single'
    
    # def get_success_url(self, *args, **kwargs):
    #     if self.object is not None:
    #         if self.object.id:
    #             return reverse('project_single', kwargs={'pk':self.object.id})
    #     return super().get_success_url(*args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form = self.get_form()
    #     if form.is_valid():
    #         self.form_valid(form)
    #         return JsonResponse({'navigate':self.get_success_url()})
    #     else:
    #         return self.form_invalid(form)
    
# remove
class ProjectRemoveView(LoginRequiredMixin, BSModalDeleteView):
    model = models.Project
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('project_index')




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
    
class InstitutionCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = InstitutionModelForm
    success_message = 'Success: Project was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    model = models.Institution_Participant

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            form = self.form_class(initial={'project': kwargs['pk']})
        elif 'institution' in kwargs:
            form = self.form_class(initial={'institution': kwargs['institution']})
        else:
            form = self.form_class()
        
        context = {'form': form}
        return render(request, self.template_name , context)

class InstitutionDirectCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = InstitutionModelFormDirect
    success_message = 'Success: Project was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    model = models.Institution
     
class InstitutionUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.Institution
    template_name = 'form_validate_base.html'
    form_class = InstitutionModelFormDirect
    success_message = 'Success: Leave was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"

# ===================== For Infos =========================
class ProjectInfoCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = GenericInfoProjectForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    model = models.GenericInfoProject

    def get(self, request, *args, **kwargs):
        if 'project' in kwargs:
            form = self.form_class(initial={'project': kwargs['project']})
        else:
            form = self.form_class()
        
        context = {'form': form}
        return render(request, self.template_name , context)

class ProjectInfoUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.GenericInfoProject
    template_name = 'form_validate_base.html'
    form_class = GenericInfoProjectForm
    success_message = 'Success: Info was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    
class ProjectInfoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = models.GenericInfoProject
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('employee')
    
    def get_success_url(self):
        previous = self.request.META.get('HTTP_REFERER')
        return previous
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)
    
    
class GenericInfoTypeProjectCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = GenericInfoTypeProjectForm
    success_message = 'Success: Project was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    model = models.GenericInfoTypeProject
    
    
class GenericInfoTypeProjectUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = models.GenericInfoTypeProject    
    template_name = 'form_validate_base.html'
    form_class = GenericInfoTypeProjectForm
    success_message = 'Success: Leave was updated.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"