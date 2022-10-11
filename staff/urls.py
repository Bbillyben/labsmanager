from django.urls import include, path, re_path
from .views import EmployeeIndexView, EmployeeView

urlpatterns = [
    path('employee/', EmployeeIndexView.as_view(), name='employee_index'),
    path('', EmployeeIndexView.as_view(), name='staff'),
    path('employee/<int:pk>', EmployeeView.as_view(), name='employee'),
]
