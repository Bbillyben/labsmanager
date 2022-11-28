from http.client import HTTPResponse
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.db.models import Q

from project.models import Participant, Project
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from . import serializers  # UserSerializer, GroupSerializer, EmployeeSerialize, EmployeeStatusSerialize, ContractEmployeeSerializer, TeamSerializer, ParticipantSerializer, ProjectSerializer
from staff.models import Employee, Employee_Status, Team, TeamMate
from expense.models import Expense_point, Contract, Contract_expense
from fund.models import Fund, Fund_Item

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from dashboard import utils
from labsmanager.utils import str2bool
from staff.filters import EmployeeFilter
from expense.filters import ContractFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Employee to be viewed or edited.
    """
    queryset = Employee.objects.select_related('user').all()
    serializer_class = serializers.EmployeeSerialize
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmployeeFilter
    
    def filter_queryset(self, queryset):
        params = self.request.query_params
        queryset = super().filter_queryset(queryset)

        is_active = params.get('active', None)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        
        name = params.get('name', None)
        if name:
            queryset = queryset.filter( Q(first_name__icontains=name) | Q(last_name__icontains=name))
             
        empStatus = params.get('status', None)
        if empStatus:
            inS=Employee_Status.objects.filter(type=empStatus).values('employee')
            queryset = queryset.filter(pk__in=inS)
        
        return queryset
    
    
    @action(methods=['get'], detail=True,url_path='status', url_name='status')
    def status(self, request, pk=None):
        status = Employee_Status.objects.filter(employee=pk).order_by('end_date')
        return JsonResponse(serializers.EmployeeStatusSerialize(status,many=True).data, safe=False)
    
    @action(methods=['get'], detail=True,url_path='contracts', url_name='contracts')
    def contracts(self,request, pk=None):
        emp = self.get_object()
        contract=Contract.objects.filter(employee=emp.pk).order_by('end_date')
        return JsonResponse(serializers.ContractSerializer(contract, many=True).data, safe=False)
    
    
    @action(methods=['get'], detail=True, url_path='teams', url_name='teams')
    def teams(self, request, pk=None):
        emp = self.get_object()
        t1=Team.objects.filter(leader=emp.pk)
        tm = TeamMate.objects.filter(employee=emp.pk).values('team')
        t2=Team.objects.filter(pk__in=tm)
        t=t1.union(t2)
        
        return JsonResponse(serializers.TeamSerializer(t, many=True).data, safe=False)
    
    @action(methods=['get'], detail=True, url_path='projects', url_name='projects')
    def projects(self, request, pk=None):
        emp = self.get_object()
        t1=Participant.objects.filter(employee=emp.pk)
        
        return JsonResponse(serializers.ParticipantSerializer(t1, many=True).data, safe=False)
    


    
