from asyncio import constants
from pydoc import doc
from .models import Project
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.http import HttpResponse

def ajax_project(request):
    if request.method == 'GET':
        datas=request.GET

    elif request.method == 'POST':
        datas=request.POST
    else:
        raise Exception("Only get and Post are processed") 
    
    print("[ajax_project] :"+ datas['action_type'])
    
    if datas['action_type'] == 'activate_project_true':
        pkU=datas['pk']
        proj = Project.objects.get(pk=pkU)
        if proj:
            proj.status = True
            proj.save()
            print("activate_project_true :"+str(proj)+" -  "+str(pkU))
    elif datas['action_type'] == 'activate_project_false':
        pkU=datas['pk']
        proj = Project.objects.get(pk=pkU)
        if proj:
            proj.status = False
            proj.save()
            print("activate_project_false :"+str(proj)+" -  "+str(pkU))  
    else:
        print("================== >>>>  AJAX STAFF COMMAND NOT FOUDN "+datas['action_type']+"  <<<< ==============================")
        
    return JsonResponse({"status":"ok,"}, safe=False)