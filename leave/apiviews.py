from django.http import JsonResponse
from django.db.models import Q, F, ExpressionWrapper, fields
from django.db.models.functions import Cast, Coalesce, Now, Extract, Abs
import datetime

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from labsmanager import serializers 

from .models import Leave, Leave_Type
from staff.models import TeamMate, Employee_Status, Team
from project.models import Participant


from django.views.decorators.csrf import csrf_exempt
from collections.abc import Iterable

from .resources import LeaveItemResources
from labsmanager.helpers import DownloadFile
import logging
logger=logging.getLogger("labsmanager")
class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.select_related('employee', 'type').all()
    serializer_class = serializers.LeaveSerializerBasic
    permission_classes = [permissions.IsAuthenticated]
    
    def filter_queryset(self, queryset):
        
        data={}
        if self.request.data:
            data.update(self.request.data)
        if self.request.query_params:
            for key in self.request.query_params:
                data[key]=self.request.query_params.get(key)
                
        if not data:
            return self.plugin_filter_queryset(queryset, self.request.user, data)
        
        qset=queryset
        types= data.get('type', None)
        exact = data.get('type_exact', False)
        if types is not None:
            if isinstance(types, str):
                types=types.split(',')
            elif not isinstance(types, Iterable):
                types=[types,]
                 
            if all([isinstance(item, int) for item in types]) or all([item.isdigit() for item in types]):
                if exact:
                    ltype = Leave_Type.objects.filter(pk__in=types)
                else:
                    ltype = Leave_Type.objects.get_queryset_descendants(Leave_Type.objects.filter(pk__in=types), include_self=True)
                qset= qset.filter(type__in=ltype)
            else:
                qset= qset.filter(type__short_name__in=types)
                     
        emp= data.get('employee', None)
       
        if emp is not None:
            if isinstance(emp, str):
                emp=emp.split(',')
            elif not isinstance(emp, Iterable):
                emp=[emp,]
            qset= qset.filter(employee__in=emp)
            
        emp_status= data.get('emp_status', None)
        if emp_status is not None and emp_status.isdigit() :
            empS=Employee_Status.current.filter(type=emp_status).values('employee')
            qset= qset.filter(employee__in=empS)
        
        team = data.get('team', None)
        if team is not None and team.isdigit():
            tm = TeamMate.objects.filter(team=team).values('employee')
            tl=Team.objects.filter(pk=team).values("leader")
            qset= qset.filter(Q(employee__in=tm) | Q(employee__in=tl))
            
            
        project = data.get('project', None)
        if project is not None:
            pa = Participant.objects.filter(project=project).values('employee')
            qset= qset.filter(Q(employee__in=pa))
        
        start_date= data.get('start', None) 
        if start_date is not None:
            if isinstance(start_date, list):
                start_date=start_date[0] 
            start_date=start_date.split("T")[0]
            query=Q(start_date__gte=start_date) | (Q(start_date__lt=start_date) & Q(end_date__gte=start_date))
            qset= qset.filter(query)
        
        end_date= data.get('end', None) 
        if end_date is not None:
            if isinstance(end_date, list):
                end_date=end_date[0]
            end_date=end_date.split("T")[0]
            query=Q(end_date__lte=end_date) | (Q(start_date__lt=end_date) & Q(end_date__gte=end_date))
            qset= qset.filter(query)
            
        today_event = data.get('showResEventRadio', None) 
        if today_event is not None and today_event == "today_event":
            today = datetime.date.today()
            query=Q(end_date__gte=today) & (Q(start_date__lte=today) )
            qset= qset.filter(query)
        
        return self.plugin_filter_queryset(qset, self.request.user, data)
        
    def plugin_filter_queryset(self, qset, user,  filters_data):
        from plugin import registry
        for plugin in registry.with_mixin("calendarevent", active=True):
           try:
               qset = plugin.filter_queryset(qset, user,  filters_data)
           except Exception as e:
               logger.warning(f"Error Filtering Leaves by plugin {plugin.name} : {e}")
        return qset
    
    def data(self, request, format=None):
        return Response("ok")
    
    def list(self, request, *args, **kwargs):
        export = request.GET.get('export', None)
        if export is not None:
            qs = self.filter_queryset(self.get_queryset())
            return self.download_queryset(qs, export)
        return super().list( request, *args, **kwargs)
    
    def download_queryset(self, queryset, export_format):
        """Download the filtered queryset as a data file"""
        dataset = LeaveItemResources().export(queryset=queryset)
        filedata = dataset.export(export_format)
        dateSuffix=datetime.datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"LeaveItem_{dateSuffix}.{export_format}"
        return DownloadFile(filedata, filename)
    
    @action(methods=['get'], detail=False, url_path='employee/(?P<emp_pk>[^/.]+)', url_name='employee')
    def search_employee(self, request, emp_pk=None):
        request.data.update({"employee":int(emp_pk),})
        qset=self.filter_queryset(self.queryset) 
        
        export = request.GET.get('export', None)
        if export is not None:
            qs = self.filter_queryset(qset)
            return self.download_queryset(qs, export)
        
        return Response(serializers.LeaveSerializer1D(qset, many=True).data)
    
    
    @action(methods=['get'], detail=False, url_path='calendar', url_name='search-calendar')
    def search_calendar(self, request):
        qset=self.filter_queryset(self.queryset) 
        
        export = request.GET.get('export', None)
        if export is not None:
            qs = self.filter_queryset(qset)
            return self.download_queryset(qs, export)   
        
        
        is_cal=request.data.get('cal',  request.query_params.get('cal', None))
        
        if request.data.get('cal', None) or request.query_params.get('cal', None):
            return Response(serializers.LeaveSerializer1DCal(qset, many=True).data)
        else:
            return Response(serializers.LeaveSerializer1D(qset, many=True).data)
    
    @action(methods=['post'], detail=False, url_path='search', url_name='search')
    def search(self, request):
        qset=self.filter_queryset(self.queryset)   
        return Response(serializers.LeaveSerializer1D(qset, many=True).data)
