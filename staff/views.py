from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Employee, Team, TeamMate
from .filters import EmployeeFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.functional import cached_property
from view_breadcrumbs import BaseBreadcrumbMixin 

# Create your views here.


class EmployeeIndexView(LoginRequiredMixin,BaseBreadcrumbMixin , TemplateView):
    template_name = 'employee/employee_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Employee
    crumbs = [("Employee","employee")]
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the Employee view:
            - employees : list of employee
        """
        context = super().get_context_data(**kwargs).copy()

        # View top-level categories
        employees = Employee.objects.all()
                 
        context['employees'] = employees

        return context


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
        
        # teams where he is leader
        teams=Team.objects.filter(leader=id)
        if teams:
            context['team_leader']=teams
        
        #teams where he is participant
        participant = TeamMate.objects.filter(employee=id)
        if participant:
            context['team_part']=participant
            
        # View top-level categories
        return context
    
    