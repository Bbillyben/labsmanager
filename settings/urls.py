from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.SettingsView.as_view(), name='settings'),
]

