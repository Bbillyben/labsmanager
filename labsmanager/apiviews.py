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
    



    
