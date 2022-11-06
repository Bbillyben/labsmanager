from http.client import HTTPResponse
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.db.models import Q

from project.models import Participant, Project
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from . import serializers  # UserSerializer, GroupSerializer, EmployeeSerialize, EmployeeStatusSerialize, ContractEmployeeSerializer, TeamSerializer, ParticipantSerializer, ProjectSerializer
from staff.models import Employee, Employee_Status, Team, TeamMate
from expense.models import Expense_point, Contract, Contract_expense
from fund.models import Fund, Fund_Item

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from dashboard import utils

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
    
    
    
    @action(methods=['get'], detail=True,url_path='status', url_name='status')
    def status(self, request, pk=None):
        print('EmployeeViewSet / status :'+str(pk))
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
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectFullSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='participant', url_name='praticipant')
    def participant(self, request, pk=None):
        proj = self.get_object()
        t1=Participant.objects.filter(project=proj.pk)
        return JsonResponse(serializers.ParticipantProjectSerializer(t1, many=True).data, safe=False)

    @action(methods=['get'], detail=True, url_path='funds', url_name='funds')
    def funds(self, request, pk=None):
        proj = self.get_object()
        t1=Fund.objects.filter(project=proj.pk)
        return JsonResponse(serializers.FundProjectSerialize(t1, many=True).data, safe=False)   
    
    @action(methods=['get'], detail=True,url_path='contracts', url_name='contracts')
    def contracts(self,request, pk=None):
        fund=Fund.objects.filter(project=pk).values('pk')        
        contract=Contract.objects.filter(fund__in=fund).order_by('end_date')
        return JsonResponse(serializers.ContractSerializer(contract, many=True).data, safe=False)

class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.select_related('funder', 'institution').all()
    serializer_class = serializers.FundSerialize
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='items', url_name='items')
    def items(self, request, pk=None):
        fund = self.get_object()
        t1=Fund_Item.objects.select_related('type').filter(fund=fund.pk)
        return JsonResponse(serializers.FundItemSerialize_min(t1, many=True).data, safe=False)
    
    
    @action(methods=['get'], detail=True, url_path='expense_timepoint', url_name='expense_timepoint')
    def fundBudgetPOint(self, request, pk=None):
        BP = Expense_point.get_lastpoint_by_fund(pk)
        return JsonResponse(serializers.ExpensePOintSerializer(BP, many=True).data, safe=False) 
    
    @action(methods=['get'], detail=False, url_path='stale', url_name='stale_fund')
    def staleFunds(self, request, pk=None):
        q_objects = Q(is_active=True) & Q(project__status=True) # base Q objkect
        slot = utils.getDashboardTimeSlot(request)
        if 'from' in slot:
            q_objects = q_objects & Q(end_date__gte=slot["from"])
        if 'to' in slot:
            q_objects = q_objects & Q(end_date__lte=slot["to"])
            
        fund=Fund.objects.select_related('project', 'funder', 'institution').filter( q_objects).order_by('-end_date')
        
        return JsonResponse(serializers.FundStaleSerializer(fund, many=True).data, safe=False) 
        
    
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(methods=['get'], detail=True, url_path='contract_expense', url_name='contract_expense')
    def items(self, request, pk=None):
        cont = self.get_object()
        t1=Contract_expense.objects.filter(contract=cont.pk)
        return JsonResponse(serializers.ContractExpenseSerializer_min(t1, many=True).data, safe=False) 

    @action(methods=['get'], detail=False, url_path='stale', url_name='contract_stale')
    def get_stale(self, request):
        dateL=date.today()+ relativedelta(months=+3)
        cont=Contract.objects.select_related('employee', 'fund', 'contract_type').filter(Q(is_active=True)& Q(fund__project__status=True)  & Q(end_date__lte=dateL)).order_by('-end_date')
        return JsonResponse(serializers.ContractSerializer(cont, many=True).data, safe=False) 
        

class BudgetPOintViewSet(viewsets.ModelViewSet):
    queryset = Expense_point.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ExpensePOintSerializer
    
