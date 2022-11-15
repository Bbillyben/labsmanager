from django.http import JsonResponse
from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from labsmanager import serializers  # UserSerializer, GroupSerializer, EmployeeSerialize, EmployeeStatusSerialize, ContractEmployeeSerializer, TeamSerializer, ParticipantSerializer, ProjectSerializer
from expense.models import Expense_point, Contract, Contract_expense


from labsmanager.utils import str2bool
from staff.filters import EmployeeFilter
from expense.filters import ContractFilter
from project.models import Project
from fund.models import Fund

class BudgetPOintViewSet(viewsets.ModelViewSet):
    queryset = Expense_point.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ExpensePOintSerializer
    
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContractFilter
    
    def filter_queryset(self, queryset):
        params = self.request.query_params
        print("[ContractViewSet.filter_queryset] start filtering")
        queryset = super().filter_queryset(queryset)
        
        is_active = params.get('active', None)
        print("[ContractViewSet.filter_queryset] is_active:"+str(is_active))
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        
        name = params.get('name', None)
        print("[ContractViewSet.filter_queryset] name:"+str(name))
        if name:
            queryset = queryset.filter( Q(employee__first_name__icontains=name) | Q(employee__last_name__icontains=name))
        
        typeC = params.get('type', None)
        print("[ContractViewSet.filter_queryset] type:"+str(typeC))
        if typeC :
            queryset = queryset.filter(contract_type=typeC)
            
            
        pname = params.get('project_name', None)
        print("[ContractViewSet.filter_queryset] name:"+str(pname))
        if pname:
            pjFund=Fund.objects.filter(project__name__icontains=pname).values('pk')
            queryset = queryset.filter(fund__in=pjFund)
            
        funder = params.get('funder', None)  
        print("[ContractViewSet.filter_queryset] funder:"+str(funder))   
        if funder is not None :
            pjF=Fund.objects.filter(funder=funder).values('pk')
            queryset = queryset.filter(fund__in=pjF)
            
        institution_name= params.get('institution_name', None)  
        print("[ContractViewSet.filter_queryset] institution_name:"+str(institution_name))   
        if institution_name is not None :
            pjI=Fund.objects.filter(institution=institution_name).values('pk')
            queryset = queryset.filter(fund__in=pjI)
        
        isStale = params.get('stale', None)
        print("[ContractViewSet.filter_queryset] isStale:"+str(isStale))
        
        if isStale is not None :
            if str2bool(isStale):
                queryset = queryset.filter(Contract.staleFilter())
            else:
                queryset = queryset.exclude(Contract.staleFilter())
        return queryset
    
    @action(methods=['get'], detail=True, url_path='contract_expense', url_name='contract_expense')
    def items(self, request, pk=None):
        cont = self.get_object()
        t1=Contract_expense.objects.filter(contract=cont.pk)
        return JsonResponse(serializers.ContractExpenseSerializer_min(t1, many=True).data, safe=False) 

    @action(methods=['get'], detail=False, url_path='stale', url_name='contract_stale')
    def get_stale(self, request):
        cont=Contract.objects.select_related('employee', 'fund', 'contract_type').filter( Q(fund__project__status=True)  & Contract.staleFilter()).order_by('-end_date')
        return JsonResponse(serializers.ContractSerializer(cont, many=True).data, safe=False) 
        