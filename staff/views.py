from http.client import HTTPResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import Q
# from django.views.generic import ListView
from .models import Employee, Team, TeamMate, Employee_Status, Employee_Superior, Employee_Type, GenericInfo
from .filters import EmployeeFilter
from expense.models import Contract
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,AccessMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.functional import cached_property
from view_breadcrumbs import BaseBreadcrumbMixin, DetailBreadcrumbMixin 
from labsmanager.mixin import TableViewMixin, CrumbListMixin

from django.urls import reverse_lazy
from .forms import EmployeeModelForm, EmployeeStatusForm,GenericInfoForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView

from django.http import HttpResponseRedirect 
from django.urls import reverse
from labsmanager.mixin import CreateModalNavigateMixin
from operator import attrgetter
from labsmanager.views_modal import BSmodalDeleteViwGenericForeingKeyMixin
import logging
logger= logging.getLogger("labsmanager")

class EmployeeIndexView(LoginRequiredMixin, BaseBreadcrumbMixin,TemplateView):
    template_name = 'employee/employee_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Employee
    crumbs = [(_("Employee"),_("employee"))]


class EmployeeView(LoginRequiredMixin, AccessMixin, CrumbListMixin,  BaseBreadcrumbMixin ,  TemplateView):
    template_name = 'employee/employee_single.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Employee
    # for CrumbListMixin
    reverseURL="employee"
    crumbListQuerySet=Employee.objects.filter(is_active=True)
    crumbListPerm=(
        #'common.employee_list',
        'staff.view_employee',
    )
    names_val=['first_name', 'last_name']
    # crumbs = [("Employee","./",),("employees",reverse("employee"))]
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.is_staff or request.user.has_perm('staff.view_employee'):
            return super().dispatch(request, *args, **kwargs)
        
        emp = Employee.objects.get(pk=kwargs['pk'])
        if request.user == emp.user or request.user.has_perm("staff.change_employee", emp):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('employee_index'))
    
        
        
    @cached_property
    def crumbs(self):
        if self.has_crumb_permission() or self.request.user.has_perm('common.employee_list'):
            return [(_("Employee"),"./",) ,
                (str(self.construct_crumb()) ,  ("A1","L1")),
                ]
        return [(_("Employee"),"",) ,
                (str(self.construct_crumb()) ,  ("A1","L1")),
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

        contracts = Contract.effective.filter(employee=id)
        if contracts:
            context['contracts']=contracts
         
        #Generic Info
        info=GenericInfo.objects.filter(employee=id)
        if info:
            context['info']=info
        # View top-level categories
        return context




###    FOR MODAL Modification EMPLOYEE

class EmployeeCreateView(LoginRequiredMixin, CreateModalNavigateMixin):
    template_name = 'form_base.html'
    form_class = EmployeeModelForm
    success_message = 'Success: Employee was created.'
    success_url = reverse_lazy('employee_index')
    
    success_single = 'employee'
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if not request.user.has_perm("staff.change_employee"):
            try:
                emp = Employee.objects.get(user= request.user)
                sup = Employee_Superior.objects.create(
                    employee = self.object, 
                    superior = emp, 
                )
            except Exception as e:
                logger.debug(f"Unable to create Employee superior from user {request.user} for employee : {self.object}")
                logger.debug(f" ERROR : {e}")
        return response

# Update
class EmployeeUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Employee
    template_name = 'form_validate_base.html'
    form_class = EmployeeModelForm
    success_message = 'Success: Employee was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"

# remove
class EmployeeRemoveView(LoginRequiredMixin, BSmodalDeleteViwGenericForeingKeyMixin, BSModalDeleteView):
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
        
    def post(self, *args, **kwargs):
        
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("okok", status=200)


# ===================== For Infos =========================
class EmployeeInfoCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'form_base.html'
    form_class = GenericInfoForm
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

class EmployeeInfoUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = GenericInfo
    template_name = 'form_validate_base.html'
    form_class = GenericInfoForm
    success_message = 'Success: Info was updated.'
    success_url = reverse_lazy('employee_index')
    label_confirm = "Confirm"
    
class EmployeeInfoDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = GenericInfo
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
    
## Get the template for activation/ deactivation user
def get_employee_valid(request, pk):
    emp = Employee.objects.filter(pk=pk).first()
    return render(request, 'staff/employee_desc_table.html', {'employee': emp})

## Get the employee info table
def get_employee_info_table(request, pk):
    info=GenericInfo.objects.filter(employee__pk=pk)
    emp = Employee.objects.filter(pk=pk).first() # required for template tag right management
    return render(request, 'employee/employee_info_table.html', {'employee':emp, 'infoEmployee': info})

## Get the employee info table
def get_employee_organisation_chart_modal(request, pk):
    return render(request, 'employee/org_chart_modal.html', {'employeePK': pk})

def get_employee_teams_lead(request, pk):
    return render(request, 'employee/emp_teal_lead_modal.html', {'employeePK': pk})

# TEAMS views
class TeamIndexView(LoginRequiredMixin, BaseBreadcrumbMixin,TemplateView):
    template_name = 'team/team_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Team
    crumbs = [(_("Teams"),"teams")]
        

class TeamView(LoginRequiredMixin, CrumbListMixin, BaseBreadcrumbMixin ,  TemplateView):
    template_name = 'team/team_single.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Team
    # for CrumbListMixin
    reverseURL="team_single"
    crumbListQuerySet=Team.objects.all()
    names_val=['name']
    crumbListPerm=(
        #'common.employee_list',
        'staff.view_team',
    )
    
    @cached_property
    def crumbs(self):
        return [(_("Team"),"./",) ,
                (str(self.construct_crumb()) ,  reverse("team_index" ) ),
                ]

    def construct_crumb(self):
        emp = Team.objects.get(pk=self.kwargs['pk'])
        return emp
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the Employee view:
            - employee : the employee corresponding
        """
        context = super().get_context_data(**kwargs).copy()

        if not 'pk' in kwargs:
            return context

        id=kwargs.get("pk", None)
        team = Team.objects.filter(pk=id)
        context['team'] = team.first()

        # View top-level categories
        return context
    
    
def get_team_resume(request, pk):
    team = Team.objects.filter(pk=pk).first()
    data = {'team': team}
    
    return render(request, 'team/team_desc_table.html', data)

def get_team_mate(request, pk):
    teamMate = TeamMate.objects.filter(team=pk)
    teamMate = TeamMate.annotate_queryset(teamMate, request.user, "view")
    team = Team.objects.get(pk=pk)
    # sorted_team_mates = sorted(teamMate, key=lambda x: x.is_active, reverse=True)
    sorted_team_mates = sorted(teamMate, key=lambda x: (not x.is_active, attrgetter('employee.first_name')(x)), reverse=False)
    data = {'mates': sorted_team_mates}
    data['team']=team # required for template tag rules
    
    return render(request, 'team/team_mate_table.html', data)

# For Organisation Chart
def get_organisation_chart_view(request):
    return render(request, 'employee/organisation_chart.html')

class OrganisationChartView(LoginRequiredMixin, AccessMixin,  BaseBreadcrumbMixin ,  TemplateView):
    template_name = 'employee/organization_chart.html'
    home_label = '<i class="fas fa-bars"></i>'
    crumbs = [(_("Organisation Chart"),"organisation_chart")]
