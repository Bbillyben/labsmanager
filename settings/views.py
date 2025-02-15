from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import BaseBreadcrumbMixin
from django.urls import reverse, reverse_lazy

from .models import LMUserSetting, LMProjectSetting

from fund.models import Cost_Type, Fund_Institution
from staff.models import Employee_Type, GenericInfoType
from project.models import Institution, GenericInfoTypeProject

from common.models import favorite, subscription
from django.conf import settings

class SettingsView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'settings/settings.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = LMUserSetting
    crumbs = [(_("Settings"),"settings")]    
    
class SettingList_cost_type(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Cost_Type
    
    def get(self,request):
        # print("[SettingList_cost_type] - get")
        context={
            'url':reverse_lazy("api:settinglist-costtype"),
            'title':_('Cost Type'),
            'columns':[
                {'name':_('name'),'item':'name','formatter':'treeNameFormatter',},
                {'name':_('Short name'),'item':'short_name'},
                {'name':_('In Focus'),'item':'in_focus', 'formatter':'basicBoolean'},
                {'name':_('Is HR'),'item':'is_hr', 'formatter':'basicBoolean'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("fund.change_cost_type"):
            context["action"]["update"] = "update_costtype"
        if request.user.has_perm("fund.add_cost_type"):
            context["action"]["add"] = reverse('add_costtype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:fund_cost_type_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
class SettingList_fundInstitution_type(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Fund_Institution
    
    def get(self,request):
        # print("[SettingList_fundInstitution_type] - get")
        context={
            'url':reverse_lazy("api:settinglist-fundinstitution"),
            'title':_('Fund Institution'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Short name'),'item':'short_name'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("fund.change_fund_institution"):
            context["action"]["update"] = "update_fund_fund_institution"
        if request.user.has_perm("fund.add_fund_institution"):
            context["action"]["add"] = reverse('add_fundinstitution')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:fund_fund_institution_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
from expense.models import Contract_type
class SettingList_Contract_type(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Contract_type
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-contracttype"),
            'title':_('Contract Type'),
            'columns':[
                {'name':_('name'),'item':'name',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("expense.change_contract_type"):
            context["action"]["update"] = "update_contract_type"
        if request.user.has_perm("expense.add_contract_type"):
            context["action"]["add"] = reverse('add_contracttype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:expense_contract_type_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
from leave.models import Leave_Type
class SettingList_Leave_type(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Leave_Type
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-leavetype"),
            'title':_('Leave Type'),
            'columns':[
                {'name':_('name'),'item':'name','formatter':'treeNameFormatter',},
                {'name':_('Short name'),'item':'short_name'},
                {'name':_('Color'),'item':'color', 'formatter':'colorFormatter',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("leave.change_leave_type"):
            context["action"]["update"] = "update_leave_type"
        if request.user.has_perm("leave.add_leave_type"):
            context["action"]["add"] = reverse('add_leave_type')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:leave_leave_type_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
       

class SettingList_Institution(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Institution
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-projectinstitution"),
            'title':_('Institution'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Short name'),'item':'short_name'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("project.change_institution"):
            context["action"]["update"] = "update_project_institution"
        if request.user.has_perm("project.add_institution"):
            context["action"]["add"] = reverse('add_institution_direct')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:project_institution_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
    

class SettingList_Employee_Type(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = Employee_Type
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-employeetype"),
            'title':_('Employee Type'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Short name'),'item':'shortname'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("staff.change_employee_type"):
            context["action"]["update"] = "update_employeetype"
        if request.user.has_perm("staff.add_employee_type"):
            context["action"]["add"] = reverse('add_employeetype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:staff_employee_type_change'
        
        return render(request=request,template_name=self.template_name,context=context)

class SettingList_GenericInfo(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = GenericInfoType
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-genericinfotype"),
            'title':_('Generic Info Employee'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Icon'),'item':'icon_val', 'formatter':'iconFormatter'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("staff.change_genericinfotype"):
            context["action"]["update"] = "update_genericinfotype"
        if request.user.has_perm("staff.add_genericinfotype"):
            context["action"]["add"] = reverse('add_genericinfotype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:staff_genericinfotype_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
class SettingList_GenericInfoProject(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = GenericInfoTypeProject
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-genericinfotypeproject"),
            'title':_('Generic Info Project'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Icon'),'item':'icon_val', 'formatter':'iconFormatter'},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("project.change_genericinfotypeproject"):
            context["action"]["update"] = "update_genericinfotypeproject"
        if request.user.has_perm("project.add_genericinfotypeproject"):
            context["action"]["add"] = reverse('add_genericinfotypeproject')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:project_genericinfotypeproject_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
from infos.models import OrganizationInfosType, ContactInfoType, ContactType

class SettingList_OrganizationInfosType(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = OrganizationInfosType
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-organizationinfostype"),
            'title':_('Organization\'s info type'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Icon'),'item':'icon_val', 'formatter':'iconFormatter'},
                {'name':_('Type'),'item':'type','formatter':'infoTypeFormatter',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("infos.change_organizationinfostype"):
            context["action"]["update"] = "update_orgainfotype"
        if request.user.has_perm("infos.add_organizationinfostype"):
            context["action"]["add"] = reverse('add_orgainfotype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:infos_organizationinfostype_change'
        
        return render(request=request,template_name=self.template_name,context=context)

class SettingList_ContactInfosType(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = ContactInfoType
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-contactinfostype"),
            'title':_('Contact\'s info type'),
            'columns':[
                {'name':_('name'),'item':'name',},
                {'name':_('Icon'),'item':'icon_val', 'formatter':'iconFormatter'},
                {'name':_('Type'),'item':'type','formatter':'infoTypeFormatter',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("infos.change_contactinfotype"):
            context["action"]["update"] = "update_contactinfotype"
        if request.user.has_perm("infos.add_contactinfotype"):
            context["action"]["add"] = reverse('add_contactinfotype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:infos_contactinfotype_change'
        return render(request=request,template_name=self.template_name,context=context)
    
class SettingList_ContactType(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = ContactType
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-contacttype"),
            'title':_('Contact type'),
            'columns':[
                {'name':_('name'),'item':'name',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("infos.change_contacttype"):
            context["action"]["update"] = "update_contacttype"
        if request.user.has_perm("infos.add_contacttype"):
            context["action"]["add"] = reverse('add_contacttype')
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:infos_contacttype_change'
                    
        return render(request=request,template_name=self.template_name,context=context)   
    
class Subscription_List(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = subscription
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:subscription-current_user"),
            'title':_('Subscriptions'),
            'columns':[
                #{'name':_('User'),'item':'user.username',},
                {'name':_('Type'),'item':'content_type.modelname','formatter':'subsTypeIconFormatter',},
                {'name':_('Item'),'item':'object_name','formatter':'subObjectUrlFormatter',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("common.delete_subscription"):
            context["action"]["delete"] = "delete_subscription"
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:common_subscription_change'
        
        return render(request=request,template_name=self.template_name,context=context)

class Favorite_List(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = favorite
    def get(self,request):
        context={
            'url':reverse_lazy("api:favorite-current_user"),
            'title':_('Favorites'),
            'columns':[
                #{'name':_('User'),'item':'user.username',},
                {'name':_('Type'),'item':'content_type.modelname','formatter':'subsTypeIconFormatter',},
                {'name':_('Item'),'item':'object_name','formatter':'subObjectUrlFormatter',},
            ], 
            'action':{
            },
            'options':{
            },         
        }
        if request.user.has_perm("common.delete_favorite"):
            context["action"]["delete"] = "delete_favorite"
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:common_favorite_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
from django.contrib.auth.models import User    
class EmployeeUser_list(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = User
    
    def get(self,request):
   
        context={
            'url':reverse_lazy("api:settinglist-employeeuser"),
            'title':_('Users'),
            'columns':[
                #{'name':_('User'),'item':'user.username',},
                {'name':_('User'),'item':'username','formatter':'userAdminSettingFormatter', 'class':'fit-content'},
                {'name':_('Last Login'),'item':'last_login','formatter':'baseDateTimeFormatter'},
                {'name':_('Groups'),'item':'groups','formatter':''},
                {'name':_('Employee'),'item':'employee','formatter':'employeeFormatter'},
                {'name':_('Is active'),'item':'is_active','formatter':'simpleFormatter'},
            ], 
            'action':{
               
            },
            'options':{
            },         
        }
        if request.user.is_staff :
            context["action"]["update"] = 'update_user_employee'
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:auth_user_change'
        
        return render(request=request,template_name=self.template_name,context=context)

class InvitationUser_list(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = User
    
    def get(self,request):
   
        context={
            'url':reverse_lazy("api:settinglist-userinvitation"),
            'title':_('Invitations'),
            'columns':[
                #{'name':_('User'),'item':'user.username',},
                {'name':_('Email'),'item':'email', 'class':'fit-content'},
                {'name':_('Date Created'),'item':'created','formatter':'baseDateTimeFormatter'},
                {'name':_('Date Sent'),'item':'sent','formatter':'baseDateTimeFormatter'},
                {'name':_('Accepted'),'item':'accepted','formatter':'basicBoolean'},
                {'name':_('Inviter'),'item':'inviter', 'formatter':'userSimpleFormatter', },
                
            ], 
            'action':{
                'add':reverse('lab_send_invite'),
            },
            'options':{
            },         
        }
        if request.user.is_staff :
            context["action"]["update"] = 'update_user_employee'
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:auth_user_change'
        
        return render(request=request,template_name=self.template_name,context=context)
    
def get_project_setting_modal(request, proj):
        
    context={
        "project":proj,
        }
    
    return render(request=request,template_name="settings/modal_project_settings.html",context=context)

from notification.models import UserNotification
class UserNotification_list(LoginRequiredMixin, TemplateView):
    template_name = 'settings/setting_table.html'
    model = UserNotification
    
    def get(self,request):
        context={
            'url':reverse_lazy("api:settinglist-pendingnotification"),
            'title':_('Pending Notifications'),
            'columns':[
                {'name':_('User'),'item':'user.username',},
                {'name':_('Content TYpe '),'item':'source_content_type.modelname', 'class':'fit-content'},
                {'name':_('Action_type'),'item':'action_type','formatter':''},
                {'name':_('Object'),'item':'source_object','formatter':''},
                {'name':_('Created'),'item':'creation','formatter':'baseDateTimeFormatter'},
            ], 
            'action':{
                # 'add':reverse('lab_send_invite'),
            },
            'options':{
            },         
        }
        # if request.user.is_staff :
        #     context["action"]["update"] = 'update_user_employee'
        if request.user.is_staff :
            context["action"]["admin"] = 'admin:notification_usernotification_change'
        
        return render(request=request,template_name=self.template_name,context=context)



## for invitation process
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalFormView
from labsmanager.utils import is_ajax
from invitations.models import Invitation
from invitations.views import SendInvite
from .forms import labInviteForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

class labInvitationCreateView(LoginRequiredMixin, BSModalFormView, SendInvite):
    model = Invitation
    form_class= labInviteForm
    success_message = 'Success: Invitation was created.'
    success_url = reverse_lazy('project_index')
    label_confirm = "Confirm"
    # template_name = "invitations/forms/_invite.html"
    template_name = 'form_base.html'
    
    from labsmanager.utils import is_ajax
    
    # def post(self, request, *args, **kwargs):
    #     print("#######################  labInvitationCreateView POST ")
    #     return super().post(request, *args, **kwargs)
    
    # def form_valid(self, form):
    #     email = form.cleaned_data["email"]
        
    #     if is_ajax(self.request.META):
    #         if form.is_valid():
    #             return self.render_to_response(
    #                 self.get_context_data(
    #                     success_message=_("%(email)s has been invited") % {"email": email},
    #                 ),
    #             )
    #         else:
    #             return self.form_invalid(form)
        
        
    #     try:
    #         invite = form.save(email)
    #         invite.inviter = self.request.user
    #         invite.save()
    #         invite.send_invitation(self.request)
    #     except Exception:
    #         return self.form_invalid(form)
    #     return self.render_to_response(
    #         self.get_context_data(
    #             success_message=_("%(email)s has been invited") % {"email": email},
    #         ),
    #     )