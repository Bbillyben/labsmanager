from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def isUserTeamLeader(context, dynvarname):
    """ Returns the value of dynvarname into the context """
    return context.get("user_"+str(dynvarname), None)


@register.simple_tag(takes_context=True)
def quotityFormat(context, dynvarname):
    """ Returns the value of dynvarname into the context """
    
    if dynvarname != None:
        val = "{0:.0%}".format(dynvarname)
        if dynvarname > 1:
            html="<div class='warning-quotity'>"+val+"</div>"
        else :
            html="<div class=''>"+val+"</div>"
    else:
        html="-"
        
    return mark_safe(html)

@register.simple_tag(takes_context=True)
def moneyFormat(context, dynvarname):
    """ Returns the value of dynvarname into the context """
    if dynvarname != None:
        val =  "{:0,.0f}€".format(dynvarname).replace(',', ' ') 
    else:
         val="-" 
    return mark_safe(val)


@register.simple_tag(takes_context=True)
def etpFormat(context, dynvarname):
    """ Returns the value of dynvarname into the context """
    if dynvarname != None:
        val =  "{:.1f}".format(dynvarname)
    else:
         val="-" 
    return mark_safe(val)