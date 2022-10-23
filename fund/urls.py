from django.urls import include, path, re_path
from . import views, views_modal

urlpatterns = [
    # path('', views.ProjectIndexView.as_view(), name='project_index'),
    # path('<pk>', views.ProjectView.as_view(), name='project_single'),
    
    
    # for sub template 
    path('ajax/<pk>/items/', views.get_fundItem_table, name='fund_item_table'),  # get fund item table template from Fund pk
]

#  for ajax
# urlpatterns += [
#     re_path(r'[a-z]ajax/', ajax_project, name='ajax_project'),
# ]

# for modal

urlpatterns += [
    path('ajax/funditem/add/<fund>', views_modal.FundItemCreateView.as_view(), name='add_funditem_open'),  
    path('ajax/funditem/<pk>/update', views_modal.FundItemUpdateView.as_view(), name='update_funditem_open'),  
    path('ajax/funditem/<pk>/delete', views_modal.FundItemDeleteView.as_view(), name='add_funditem_open'),
    
    path('ajax/add/<project>', views_modal.FundCreateView.as_view(), name='add_fund_open'),  
    path('ajax/<pk>/update', views_modal.FundUpdateView.as_view(), name='update_fund_open'),  
    path('ajax/<pk>/delete', views_modal.FundDeleteView.as_view(), name='add_fund_open'),
   
]