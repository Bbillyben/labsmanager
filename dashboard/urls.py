from django.urls import include, path, re_path
from . import views
urlpatterns = [
    path('fundloss', views.FundLossView.as_view(), name='loss'),
    path('fundloss/card', views.FundLossCardView.as_view(), name='loss_card'),
]
