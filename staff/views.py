from http.client import HTTPResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
# from django.views.generic import ListView
from .models import Employee, Team, TeamMate, Employee_Status, Employee_Type
from .filters import EmployeeFilter
from expense.models import Contract
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.functional import cached_property
from view_breadcrumbs import BaseBreadcrumbMixin
from labsmanager.mixin import TableViewMixin

from django.urls import reverse_lazy
from .forms import EmployeeModelForm, EmployeeStatusForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView


# Create your views here.


class EmployeeIndexView(LoginRequiredMixin, BaseBreadcrumbMixin,TemplateView):
    template_name = 'employee/employee_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Employee
    crumbs = [("Employee","employee")]



class EmployeeView(LoginRequiredMixin, BaseBreadcrumbMixin ,  TemplateView):
    template_name = 'employee/employee_single.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Employee
    # crumbs = [("Employee","./",),("employees",reverse("employee"))]

    @cached_property
    def crumbs(self):
        return [("Employee","./",) ,
                (str(self.construct_crumb()) ,  reverse("employee", kwargs={'pk':'4'} ) ),
                ]

    def construct_crumb(self):
        emp = Employee.objects.get(pk=self.kwargs['pk'])
        return emp

    def get_context_data(self, **kwargs):
        """Returns custom context data for the Employee view:
            - employee : the employee corresponding
        """
        context = super().get_context_data(**kwargs).copy()

        if not 'pk' in kwargs:
            return context

        id=kwargs.get("pk", None)
        employee = Employee.objects.filter(pk=id)
        context['employee'] = employee.first()

        # status
        status = Employee_Status.objects.filter(employee=id)
        if status:
            context['status']=status

        # teams where he is leader
        teams=Team.objects.filter(leader=id)
        if teams:
            context['team_leader']=teams

        #teams where he is participant
        participant = TeamMate.objects.filter(employee=id)
        if participant:
            context['team_part']=participant

        contracts = Contract.objects.filter(employee=id)
        if contracts:
            context['contracts']=contracts

        # View top-level categories
        return context




###    FOR MODAL Modification EMPLOYEE

class EmployeeCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = EmployeeModelForm
    success_message = 'Success: Employee was created.'
    success_url = reverse_lazy('employee_index')

# Update
class EmployeeUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Employee
    template_name = 'form_validate_base.html'
    form_class = EmployeeModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"

# remove
class EmployeeRemoveView(LoginRequiredMixin, BSModalDeleteView):
    model = Employee
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('employee_index')

class EmployeeStatusCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = EmployeeStatusForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"

    def get(self, request, *args, **kwargs):
        if 'employee' in kwargs:
            form = self.form_class(initial={'employee': kwargs['employee']})
        else:
            form = self.form_class()
        
        context = {'form': form}
        return render(request, self.template_name , context)


    
class StatusUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Employee_Status
    template_name = 'form_validate_base.html'
    form_class = EmployeeStatusForm
    success_message = 'Success: Status was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"

# remove
class StatusDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Employee_Status
    template_name = 'form_delete_base.html'
    # form_class = EmployeeModelForm
    success_url = reverse_lazy('employee')
    
    def get_success_url(self):
        previous = self.request.META.get('HTTP_REFERER')
        return previous
