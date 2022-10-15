from django.contrib.auth.models import User, Group
from rest_framework import serializers
from staff.models import Employee, Employee_Status, Employee_Type

class EmployeeTypeSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee_Type
        fields = ['pk', 'shortname', 'name', ]
        
class EmployeeStatusSerialize(serializers.HyperlinkedModelSerializer):
    type = EmployeeTypeSerialize(many=False, read_only=True)
    class Meta:
        model = Employee_Status
        fields = ['pk', 'type', 'start_date', 'end_date',]
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'first_name','last_name', 'email', 'groups', 'is_active',]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['pk', 'url', 'name']
        
class EmployeeSerialize(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    status =EmployeeStatusSerialize(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ['pk', 'user', 'birth_date', 'entry_date', 'exit_date','is_team_leader','is_team_mate','status']

