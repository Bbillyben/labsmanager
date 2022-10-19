from multiprocessing import context
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from staff.models import Employee, Employee_Status, Employee_Type, Team, TeamMate
from expense.models import Contract
from fund.models import Fund, Cost_Type, Fund_Item, Fund_Institution
from project.models import Project, Institution




 # User and Group Serailizer ########### ------------------------------------ ###########
       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'first_name','last_name', 'email', 'groups', 'is_active',]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'url', 'name']
        

# Project App Serializer  ########### ------------------------------------ ###########

class InstitutionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Institution
        fields = ['pk', 'short_name', 'name']  
        

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk', 'name', 'start_date', 'start_date', 'end_date', 'status']
        
class Institution_ParticipantSerializer(serializers.ModelSerializer):
     project=ProjectSerializer(many=False, read_only=True)
     institution=InstitutionSerializer(many=False, read_only=True)
     
     class Meta:
        model = Institution
        fields = ['pk', 'project', 'institution', 'type_part', 'status']  

# Fund App Serializer ########### ------------------------------------ ###########
class CostTypeSerialize(serializers.ModelSerializer):
     class Meta:
        model = Cost_Type
        fields = ['pk', 'short_name', 'name'] 
        
class Fund_InstitutionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Fund_Institution
        fields = ['pk', 'short_name', 'name']  

  
class FundSerialize(serializers.ModelSerializer):
    funder=Fund_InstitutionSerializer(many=False, read_only=True)
    institution=InstitutionSerializer(many=False, read_only=True)
    project=ProjectSerializer(many=False, read_only=True)
    class Meta:
        model = Fund
        fields = ['pk', 'project', 'funder', 'institution', 'ref'] 
          
class FundItemSerialize(serializers.ModelSerializer):
    fund=FundSerialize(many=False, read_only=True)
    class Meta:
        model = Fund_Item
        fields = ['pk', 'type', 'amout', 'fund']        

class ContractEmployeeSerializer(serializers.ModelSerializer):
    fund = FundSerialize(many=False, read_only=True)
    class Meta:
        model = Contract
        fields = ['pk','start_date', 'end_date', 'fund', 'quotity']
    

        
# Employee App Serializer  ########### ------------------------------------ ###########

class EmployeeTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = Employee_Type
        fields = ['pk', 'shortname', 'name', ]
        
class EmployeeStatusSerialize(serializers.ModelSerializer):
    type = EmployeeTypeSerialize(many=False, read_only=True)
    class Meta:
        model = Employee_Status
        fields = ['pk', 'type', 'start_date', 'end_date',]
        
class EmployeeSerialize(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    get_status =EmployeeStatusSerialize(many=True, read_only=True)
    contracts=ContractEmployeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = ['pk', 'user', 'birth_date', 'entry_date', 'exit_date','is_team_leader','is_team_mate','get_status','is_active',
                  'contracts', 
                  ]
        
class EmployeeSerialize_Min(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Employee
        fields = ['pk', 'user_name', 'is_active']    
        
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

