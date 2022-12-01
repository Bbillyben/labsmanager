from django.http import JsonResponse
from django.db.models import Q, F

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from labsmanager import serializers 

from .models import Fund, Fund_Item
from dashboard import utils
from expense.models import Expense_point
from project.filters import ProjectFilter
from project.models import Participant
from .resources import FundItemResource
from labsmanager.helpers import DownloadFile

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

class FundItemViewSet(viewsets.ModelViewSet):
    queryset = Fund_Item.objects.select_related('fund').all()
    serializer_class = serializers.FundItemSerialize
    permission_classes = [permissions.IsAuthenticated]        
    filter_backends = (filters.DjangoFilterBackend,)
    
    def list(self, request, *args, **kwargs):
        export = request.GET.get('export', None)
        if export is not None:
            qs = self.filter_queryset(self.get_queryset())
            return self.download_queryset(qs, export)
        return super().list( request, *args, **kwargs)
    
    def download_queryset(self, queryset, export_format):
        """Download the filtered queryset as a data file"""
        dataset = FundItemResource().export(queryset=queryset)
        filedata = dataset.export(export_format)
        filename = f"FundItems.{export_format}"
        return DownloadFile(filedata, filename)
    
    def filter_queryset(self, queryset):
        params = self.request.GET
        queryset = super().filter_queryset(queryset)
        
        fund_type = params.get('fund_type', None)
        if fund_type is not None:
            queryset = queryset.filter(type=fund_type)
        
        available = params.get('available', None)
        if available is not None:
            queryset=queryset.annotate(availableT=F('amount')+F('expense'))
            queryset = queryset.filter(Q(availableT__gte=int(available)))
        
        active = params.get('active', None)
        if active is not None:
            queryset = queryset.filter(fund__is_active=active)
        
        project_name = params.get('project_name', None)
        if project_name is not None:
            queryset = queryset.filter(fund__project__name__icontains=project_name)
            
        participant_name = params.get('participant_name', None)
        if participant_name is not None:
            pp = Participant.objects.filter(Q(employee__first_name__icontains=participant_name) | Q(employee__last_name__icontains=participant_name)).values('project')
            
            queryset = queryset.filter(fund__project__in=pp)

        institution_name= params.get('institution_name', None)
        if institution_name is not None:
            queryset = queryset.filter(fund__institution=institution_name)
        
        funder= params.get('funder', None)
        if funder is not None:
            queryset = queryset.filter(fund__funder=funder)
            
        fundref = params.get('fundref', None)
        if fundref is not None:
            queryset = queryset.filter(fund__ref__icontains=fundref)
        
        stale = params.get('stale', None)
        if stale is not None:
            q_objects = Q(fund__is_active=True) & Q(fund__project__status=True) # base Q objkect
            slot = utils.getDashboardTimeSlot(self.request)
            if 'from' in slot:
                q_objects = q_objects & Q(fund__end_date__gte=slot["from"])
            if 'to' in slot:
                q_objects = q_objects & Q(fund__end_date__lte=slot["to"])
            queryset = queryset.filter(q_objects)
        
        return queryset