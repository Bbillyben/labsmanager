from django.urls import include, path, re_path
from . import views, views_modal

urlpatterns = [
    path('', views.ContractIndexView.as_view(), name='contract_index'),
    # path('<pk>', views.ProjectView.as_view(), name='project_single'),
    
    
    # for sub template 
    path('ajax/<pk>/contract_expense/', views.get_contractExpense_table, name='contract_expense_table'),  # get fund item table template from Fund pk
]

# for modal

urlpatterns += [
    path('ajax/contract/add/', views_modal.ContractCreateView.as_view(), name='add_contract'), 
    path('ajax/contract/add/employee/<employee>', views_modal.ContractCreateView.as_view(), name='add_contract_open'), 
    path('ajax/contract/add/project/<project>', views_modal.ContractCreateView.as_view(), name='add_contract_open'),   
    path('ajax/contract/<pk>/update', views_modal.ContractUpdateView.as_view(), name='update_contract_open'),  
    path('ajax/contract/<pk>/delete', views_modal.ContractDeleteView.as_view(), name='add_contract_open'),
    
    
    path('ajax/contract_expense/add/<contract>', views_modal.ContractExpenseCreateView.as_view(), name='add_contract_expense'),
    path('ajax/contractitem/<pk>/update', views_modal.ContractExpenseUpdateView.as_view(), name='update_contractitem_open'),  
    path('ajax/contractitem/<pk>/delete', views_modal.ContractExpenseDeleteView.as_view(), name='add_contractitem_open'),
]