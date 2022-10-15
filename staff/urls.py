from django.urls import include, path, re_path
from .views import EmployeeIndexView, EmployeeUpdateView, EmployeeView, EmployeeCreateView
from .ajax import ajax_staff

urlpatterns = [
    path('employee/', EmployeeIndexView.as_view(), name='employee_index'),
    path('', EmployeeIndexView.as_view(), name='staff'),
    path('employee/<int:pk>', EmployeeView.as_view(), name='employee'),
]

#  for ajax
urlpatterns += [
    re_path(r'[a-z]*/ajax/{0,1}', ajax_staff, name='ajax_staff'),
]

# for modal

urlpatterns += [
    path('employee/add/', EmployeeCreateView.as_view(), name='create_employee'),  # modal creation employee
    path('employee/udpate/<pk>', EmployeeUpdateView.as_view(), name='update_employee'),  # modal update employee
]