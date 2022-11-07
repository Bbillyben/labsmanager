from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

# from allauth.account.views import LoginView
# Create your views here.

class redirectIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'labmanager/index.html' #'labmanager/index.html'
    def get(self, request, *args, **kwargs): ## Redirect to dash board for the moment
        return redirect('dashboard')
    
class IndexView(LoginRequiredMixin, TemplateView):
    """View for index page."""
    template_name = 'labmanager/index.html' #'labmanager/index.html'
    
    # def get(self, request, *args, **kwargs): ## Redirect to dash board for the moment
    #     return redirect('dashboard')
    
