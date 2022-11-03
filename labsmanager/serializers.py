from multiprocessing import context
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from staff.models import Employee, Employee_Status, Employee_Type, Team, TeamMate
from expense.models import Expense_point, Contract, Contract_expense, Contract_type
from fund.models import Fund, Cost_Type, Fund_Item, Fund_Institution
from project.models import Project, Institution, Participant
from django.db.models import Sum



 # User and Group Serailizer ########### ------------------------------------ ###########
       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username', 'first_name','last_name', 'email', 'groups', 'is_active',]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'url', 'name']
        
        

# ------------------------------------------------------------------------------------ #
# ---------------------------    MINIMALIST SERIALISZER    --------------------------- #
# ------------------------------------------------------------------------------------ #

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    APP PROJECT 

class InstitutionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Institution
        fields = ['pk', 'short_name', 'name']  
        

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'name', 'start_date', 'start_date', 'end_date', 'status']


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    APP FUND 

class CostTypeSerialize(serializers.ModelSerializer):
     class Meta:
        model = Cost_Type
        fields = ['pk', 'short_name', 'name'] 
        
class Fund_InstitutionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Fund_Institution
        fields = ['pk', 'short_name', 'name']  

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    APP Employee 

class EmployeeTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = Employee_Type
        fields = ['pk', 'shortname', 'name', ]

        
class EmployeeSerialize_Min(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Employee
        fields = ['pk', 'user_name', 'is_active']    
        

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    APP Expense

class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract_type
        fields = ['pk', 'name',]  


# --------------------------------------------------------------------------------------- #
# ---------------------------    APP PROJECT / SERIALISZER    --------------------------- #
# --------------------------------------------------------------------------------------- #


        
class Institution_ParticipantSerializer(serializers.ModelSerializer):
     project=ProjectSerializer(many=False, read_only=True)
     institution=InstitutionSerializer(many=False, read_only=True)
     
     class Meta:
        model = Institution
        fields = ['pk', 'project', 'institution', 'type_part', 'status']  

class ParticipantSerializer(serializers.ModelSerializer):
    status=serializers.SerializerMethodField()
    project=ProjectSerializer(many=False, read_only=True)
    # project_name=serializers.SerializerMethodField()
    # project_status=serializers.SerializerMethodField()
    # project_start_date=serializers.SerializerMethodField()
    # project_end_date=serializers.SerializerMethodField()
    # project_pk=serializers.SerializerMethodField()
    class Meta:
        model = Participant
        # fields = ['pk', 'project_pk', 'project_name', 'project_start_date', 'project_end_date', 'project_status', 'status', 'quotity' ]
        fields = ['pk', 'project', 'start_date', 'end_date', 'status', 'quotity' ]
    
    def get_status(self,obj):
        return obj.get_status_display()
    
    def get_project_name(self,obj):
        return obj.project.name
    
    def get_project_start_date(self,obj):
        return obj.project.start_date
    
    def get_project_end_date(self,obj):
        return obj.project.end_date
        
    def get_project_status(self,obj):
        return obj.project.status
    
    def get_project_pk(self,obj):
        return obj.project.pk
    


# ------------------------------------------------------------------------------------ #
# ---------------------------    APP FUND / SERIALISZER    --------------------------- #
# ------------------------------------------------------------------------------------ #

  
class FundSerialize(serializers.ModelSerializer):
    funder=Fund_InstitutionSerializer(many=False, read_only=True)
    institution=InstitutionSerializer(many=False, read_only=True)
    project=ProjectSerializer(many=False, read_only=True)
    class Meta:
        model = Fund
        fields = ['pk', 'project', 'funder', 'institution', 'ref', 'is_active',] 
          
class FundItemSerialize(serializers.ModelSerializer):
    fund=FundSerialize(many=False, read_only=True)
    type=CostTypeSerialize(many=False, read_only=True)
    class Meta:
        model = Fund_Item
        fields = ['pk', 'type', 'amount', 'fund']        

class FundStaleSerializer(serializers.ModelSerializer):
    availability=serializers.SerializerMethodField()
    project=ProjectSerializer(many=False, read_only=True)
    funder=serializers.SerializerMethodField()
    institution=serializers.SerializerMethodField()
    
    class Meta:
        model = Fund
        fields=['pk', 'project', 'funder', 'institution', 'end_date', 'availability',]
        
    def get_availability(self,obj):
        avail=obj.get_available()
        return avail['amount'].sum(axis=0, skipna=True)
    def get_project(self,obj):
        return obj.project.name
    def get_funder(self, obj):
        return obj.funder.short_name
    def get_institution(self, obj):
        return obj.institution.short_name
    
    
class FundProjectSerialize(serializers.ModelSerializer):
    funder=Fund_InstitutionSerializer(many=False, read_only=True)
    institution=InstitutionSerializer(many=False, read_only=True)
    amount =serializers.SerializerMethodField()
    
    class Meta:
        model = Fund
        fields = ['pk', 'funder', 'institution', 'start_date', 'end_date', 'ref', 'amount', 'is_active',] 
        
    def get_amount(self,obj):
        return Fund_Item.objects.filter(fund=obj.pk).aggregate(Sum('amount'))["amount__sum"]

class ExpensePOintSerializer(serializers.ModelSerializer):
    fund=FundSerialize(many=False, read_only=True)
    type=CostTypeSerialize(many=False, read_only=True)
    class Meta:
        model = Expense_point
        fields = ['pk', 'entry_date', 'value_date', 'fund', 'type', 'amount']       
# ---------------------------------------------------------------------------------------- #
# ---------------------------    APP Expense / SERIALISZER    --------------------------- #
# ---------------------------------------------------------------------------------------- #
 
class ContractSerializer(serializers.ModelSerializer):
    fund = FundSerialize(many=False, read_only=True)
    contract_type = serializers.SerializerMethodField()
    employee=EmployeeSerialize_Min(many = False, read_only = True)
    class Meta:
        model = Contract
        fields = ['pk', 'employee', 'start_date', 'end_date', 'fund', 'contract_type','total_amount', 'quotity', 'is_active',]
    
    def get_contract_type(self,obj):
        if obj.contract_type:
            return obj.contract_type.name
        return None 
    
          
class ContractExpenseSerializer_min(serializers.ModelSerializer):
    fund = FundSerialize(many=False, read_only=True)
    status = serializers.SerializerMethodField()
    type =   CostTypeSerialize(many=False, read_only=True)
    class Meta:
        model = Contract_expense
        fields = ['pk', 'date', 'type', 'status', 'fund', 'amount']
        
    def get_status(self,obj):
        return obj.get_status_display()
    
# class ContractSerializer(serializers.ModelSerializer):
#     expenses = ContractExpenseSerializer_min(many=True, read_only=True)
#     employee=EmployeeSerialize_Min(many=False, read_only=True)
#     fund=FundSerialize(many=False, read_only=True)
#     class Meta:
#         model = Contract
#         fields = ['pk', 'employee', 'start_date', 'end_date', 'quotity',  'fund',
#                   'total_amount',
#                   'expenses', ]
    
# ---------------------------------------------------------------------------------------- #
# ---------------------------    APP EMPLOYEE / SERIALISZER    --------------------------- #
# ---------------------------------------------------------------------------------------- #
        

        
class EmployeeStatusSerialize(serializers.ModelSerializer):
    type = EmployeeTypeSerialize(many=False, read_only=True)
    is_contractual=serializers.SerializerMethodField()
    class Meta:
        model = Employee_Status
        fields = ['pk', 'type', 'start_date', 'end_date', 'is_contractual']
        
    def get_is_contractual(self,obj):
        return obj.get_is_contractual_display()
     
class EmployeeSerialize(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    get_status =EmployeeStatusSerialize(many=True, read_only=True)
    contracts=ContractSerializer(many=True, read_only=True)
    projects=ParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ['pk','first_name', 'last_name', 'user', 'birth_date', 'entry_date', 'exit_date','is_team_leader','is_team_mate','get_status','is_active',
                  'contracts', 'contracts_quotity',
                  'projects','projects_quotity',
                  ]
        
class TeamMateSerializer_min(serializers.ModelSerializer):
    employee=EmployeeSerialize_Min(many=False, read_only=True)
    class Meta:
        model = TeamMate
        fields=['pk', 'employee']
    
    
class TeamSerializer(serializers.ModelSerializer):
    leader=EmployeeSerialize_Min(many=False, read_only=True)
    team_mate=TeamMateSerializer_min(many=True, read_only=True)

    
    class Meta:
        model= Team
        fields=['pk','name', 'leader', 'team_mate']





#  For project tabe

        
        
class ParticipantProjectSerializer(serializers.ModelSerializer):
    employee=EmployeeSerialize_Min(many = False, read_only = True)
    status=serializers.SerializerMethodField()
    class Meta:
        model = Participant
        fields = ['pk', 'employee', 'start_date', 'end_date', 'status', 'quotity' ]
    
    def get_status(self,obj):
        return obj.get_status_display()

class ProjectFullSerializer(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField() 
    participant_count=serializers.SerializerMethodField()
    fund=serializers.SerializerMethodField() 
    # total_amount= serializers.SerializerMethodField()
    
    
    class Meta:
        model = Project
        fields = ['pk', 'name', 'start_date', 'start_date', 'end_date', 'status', 
                  'participant', 'participant_count',
                  'fund','get_funds_amount', 
                  ]
    def get_participant(self,obj):
        part = Participant.objects.filter(project = obj.pk, employee__user__is_active= True)
        return ParticipantProjectSerializer(part , many=True).data
    
    def get_participant_count(self,obj):
        part = Participant.objects.filter(project = obj.pk, employee__user__is_active= True).count()
        return part
    
    def get_fund(self,obj):
        fund = Fund.objects.filter(project = obj.pk)
        return FundProjectSerialize(fund , many=True).data
    
    # def get_total_amount(self,obj):
    #     fund = Fund.objects.filter(project = obj.pk)
    #     return Fund_Item.objects.filter(fund__in=fund).aggregate(Sum('amount'))["amount__sum"]
    
    
    
