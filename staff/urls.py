from django.urls import include, path, re_path
from .views import EmployeeIndexView, EmployeeUpdateView, EmployeeView, EmployeeCreateView, EmployeeRemoveView, EmployeeStatusCreateView, StatusUpdateView, StatusDeleteView
from .ajax import ajax_staff

urlpatterns = [
    path('employee/', EmployeeIndexView.as_view(), name='employee_index'),
    path('', EmployeeIndexView.as_view(), name='staff'),
    path('employee/<int:pk>', EmployeeView.as_view(), name='employee'),
]

#  for ajax
urlpatterns += [
    re_path(r'[a-z]ajax/{0,1}', ajax_staff, name='ajax_staff'),
]

# for modal

urlpatterns += [
    path('employee/add/', EmployeeCreateView.as_view(), name='create_employee'),  # modal creation employee
    path('employee/<pk>/udpate', EmployeeUpdateView.as_view(), name='update_employee'),  # modal update employee
    path('employee/<pk>/delete', EmployeeRemoveView.as_view(), name='delete_employee'),  # modal delete employee
    path('employee/<employee>/status/add/', EmployeeStatusCreateView.as_view(), name='create_status_employee'),  
    path('status/<pk>/update/', StatusUpdateView.as_view(), name='update_status_employee'),  # specific for status view
    path('status/<pk>/delete/', StatusDeleteView.as_view(), name='delete_status_employee'),  # specific for status view
]