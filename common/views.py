from django.shortcuts import render, HttpResponse

from .models import favorite, subscription
from labsmanager.serializers import FavoriteSerialize
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
# Create your views here.

def get_user_fav_obj(request):
    if request.method != 'POST' or request.POST.get('type', None) == None:
        return HttpResponse("", 400)
    type=request.POST.get('type', "").split('.')
    pk=request.POST.get('pk')

    ct= ContentType.objects.get(app_label=type[0], model=type[1])
    fav=favorite.objects.filter(user=request.user, content_type=ct, object_id=pk)
    return render(request, 'favorite_star.html', {"fav":fav})

from django.apps import apps
def get_user_favorite(request):
    fav=favorite.objects.filter(user=request.user) #.order_by("content_type")
    fav = sorted(fav, key=lambda x: (x.content_type.name, x.content_object.__str__()))
    data={} #'favorites':FavoriteSerialize(fav, many=True).data}

    for el in fav:
        id = apps.get_model(el.content_type.app_label, el.content_type.model)
        id=id._meta.verbose_name.title()
        if not id in data:
            data[id]=[]
        data[id].append(el)

    for els in data:
          data[els]=FavoriteSerialize(data[els], many=True).data

    return data

def get_nav_favorites(request):

    data=get_user_favorite(request)
    return render(request, 'favorite_nav.html', {"datas":data})


def get_nav_favorites_accordion(request):

    data=get_user_favorite(request)
    return render(request, 'labmanager/index_card_favorite.html', {"datas":data})

def toggle_favorites(request):
    if request.method != 'POST':
        return HttpResponse("", 400)
    type=request.POST.get('type').split('.')
    pk=request.POST.get('pk')

    ct= ContentType.objects.get(app_label=type[0], model=type[1])
    fav=favorite.objects.filter(user=request.user, content_type=ct, object_id=pk)

    data={'fav':0}
    if fav:
        fav.delete()
    else:
        f=favorite(user=request.user,
                   content_type=ct,
                    object_id=pk
                   )
        f.save()
        data={'fav':f}


    return render(request, 'favorite_star.html', data)


##### For Subscription ####
def get_user_subscription_obj(request):
    if request.method != 'POST' or request.POST.get('type', None) == None:
        return HttpResponse("", 400)
    type=request.POST.get('type', "").split('.')
    pk=request.POST.get('pk')

    ct= ContentType.objects.get(app_label=type[0], model=type[1])
    sub=subscription.objects.filter(user=request.user, content_type=ct, object_id=pk)
    return render(request, 'subscription_bell.html', {"sub":sub})


def toggle_subscription(request):
    if request.method != 'POST':
        return HttpResponse("", 400)
    type=request.POST.get('type').split('.')
    pk=request.POST.get('pk')

    ct= ContentType.objects.get(app_label=type[0], model=type[1])
    sub=subscription.objects.filter(user=request.user, content_type=ct, object_id=pk)

    data={'sub':0}
    if sub:
        sub.delete()
    else:
        s=subscription(user=request.user,
                   content_type=ct,
                    object_id=pk
                   )
        s.save()
        data={'sub':s}


    return render(request, 'subscription_bell.html', data)



#### For email list and modification ####
def get_user_emaillist(request):
    return render(request, 'account/email_list.html')


### for email testing / to open in new window ####
from labsmanager.mails import SubscriptionMail
from django.contrib.auth.models import User
def get_test_email(request,*args, **kwargs):

    upk = request.POST["user"]
    user = User.objects.get(pk=upk)

    sm = SubscriptionMail()
    kwargs ={'user':user, 'embedImg':True}
    
    ctx = sm.generate_context(**    kwargs)
    html_message=  sm.render_html(**kwargs)
    
    return HttpResponse(html_message) #{'status': 'success', 'message': _("Mail Generated"), 'content':html_message})

