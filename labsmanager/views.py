from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class IndexView(TemplateView):
    """View for InvenTree index page."""
    template_name = 'labmanager/index.html'