from .models import Employee
import django_filters

class EmployeeFilter(django_filters.FilterSet):
    """ set filter for django.filters"""
    
    entry_date = django_filters.NumberFilter(field_name='entry_date', lookup_expr='year')
    entry_date__gt = django_filters.NumberFilter(field_name='entry_date', lookup_expr='year__gt')
    entry_date__lt = django_filters.NumberFilter(field_name='entry_date', lookup_expr='year__lt')
    
    exit_date = django_filters.NumberFilter(field_name='exit_date', lookup_expr='year')
    exit_date__gt = django_filters.NumberFilter(field_name='exit_date', lookup_expr='year__gt')
    exit_date__lt = django_filters.NumberFilter(field_name='exit_date', lookup_expr='year__lt')
    
    user__name =  django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Employee
        fields = ['user', 'entry_date', 'exit_date']
    