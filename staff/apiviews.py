from django.http import JsonResponse
from django.db.models import Q

from project.models import Participant
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from labsmanager import serializers  # UserSerializer, GroupSerializer, EmployeeSerialize, EmployeeStatusSerialize, ContractEmployeeSerializer, TeamSerializer, ParticipantSerializer, ProjectSerializer
from staff.models import Employee, Employee_Status, Team, TeamMate
from expense.models import  Contract

from labsmanager.utils import str2bool
from labsmanager.helpers import DownloadFile

from staff.filters import EmployeeFilter

from .ressources import EmployeeResource


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
    
    def list(self, request, *args, **kwargs):
        export = request.GET.get('export', None)
        if export is not None:
            qs = self.filter_queryset(self.get_queryset())
            return self.download_queryset(qs, export)
        return super().list( request, *args, **kwargs)
    
    def download_queryset(self, queryset, export_format):
        """Download the filtered queryset as a data file"""
        dataset = EmployeeResource().export(queryset=queryset)
        filedata = dataset.export(export_format)
        filename = f"Employee.{export_format}"
        return DownloadFile(filedata, filename)
        # return JsonResponse('not a test', safe=False)
    
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
    