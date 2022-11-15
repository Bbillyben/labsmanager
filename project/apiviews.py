from django.http import JsonResponse
from django.db.models import Q

from project.models import Participant, Project, Institution_Participant
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from labsmanager import serializers  # UserSerializer, GroupSerializer, EmployeeSerialize, EmployeeStatusSerialize, ContractEmployeeSerializer, TeamSerializer, ParticipantSerializer, ProjectSerializer
from expense.models import Contract
from fund.models import Fund
from labsmanager.utils import str2bool
from .filters import ProjectFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectFullSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter
    
    
    def filter_queryset(self, queryset):
        params = self.request.query_params
        print("[ProjectViewSet.filter_queryset] start filtering")
        queryset = super().filter_queryset(queryset)
        
        status = params.get('status', None)
        print("[ProjectViewSet.filter_queryset] status:"+str(status))
        if status:
            queryset = queryset.filter(status=status)
        
        pname = params.get('project_name', None)
        print("[ProjectViewSet.filter_queryset] name:"+str(pname))
        if pname:
            queryset = queryset.filter(name__icontains=pname)
            
        isStale = params.get('stale', None)
        print("[ProjectViewSet.filter_queryset] isStale:"+str(isStale))
        
        if isStale is not None :
            if str2bool(isStale):
                queryset = queryset.filter(Project.staleFilter())
            else:
                queryset = queryset.exclude(Project.staleFilter())
        
        funder = params.get('funder', None)  
        print("[ProjectViewSet.filter_queryset] funder:"+str(funder))   
        if funder is not None :
            pjF=Fund.objects.filter(funder=funder).values('project')
            queryset = queryset.filter(pk__in=pjF)
            
        participant_name= params.get('participant_name', None)  
        print("[ProjectViewSet.filter_queryset] participant_name:"+str(participant_name))   
        if participant_name is not None :
            pjP=Participant.objects.filter(Q(employee__first_name__icontains=participant_name) | Q(employee__last_name__icontains=participant_name)).values('project')
            queryset = queryset.filter(pk__in=pjP)
        
        institution_name= params.get('institution_name', None)  
        print("[ProjectViewSet.filter_queryset] institution_name:"+str(institution_name))   
        if institution_name is not None :
            pjI=Institution_Participant.objects.filter(institution=institution_name).values('project')
            queryset = queryset.filter(pk__in=pjI)
        
        return queryset
        
    @action(methods=['get'], detail=True, url_path='participant', url_name='participant')
    def participant(self, request, pk=None):
        proj = self.get_object()
        t1=Participant.objects.filter(project=proj.pk)
        return JsonResponse(serializers.ParticipantProjectSerializer(t1, many=True).data, safe=False)

    @action(methods=['get'], detail=True, url_path='institution', url_name='institution')
    def institution(self, request, pk=None):
        proj = self.get_object()
        t1=Institution_Participant.objects.filter(project=proj.pk)
        return JsonResponse(serializers.Institution_ProjectParticipantSerializer(t1, many=True).data, safe=False)

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
