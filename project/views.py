from django.shortcuts import render
from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.urls import reverse
from view_breadcrumbs import BaseBreadcrumbMixin

class ProjectIndexView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'project/project_base.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Project
    crumbs = [("Project","project")]
    
    
    
class ProjectView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):
    template_name = 'project/project_single.html'
    home_label = '<i class="fas fa-bars"></i>'
    model = Project
    # crumbs = [("Project","project")]
    
    @cached_property
    def crumbs(self):
        return [("Project","./",) ,
                (str(self.construct_crumb()) ,  reverse("project_single", kwargs={'pk':'4'} ) ),
                ]

    def construct_crumb(self):
        proj = Project.objects.get(pk=self.kwargs['pk'])
        return proj
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the Employee view:
            - employee : the employee corresponding
        """
        context = super().get_context_data(**kwargs).copy()

        if not 'pk' in kwargs:
            return context

        id=kwargs.get("pk", None)
        proj = Project.objects.filter(pk=id)
        context['project'] = proj.first()

        # View top-level categories
        return context


def get_project_resume(request, pk):
    proj = Project.objects.filter(pk=pk).first()
    data = {'project': proj}
    
    return render(request, 'project/project_desc_table.html', data)