from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def isUserTeamLeader(context, dynvarname):
    """ Returns the value of dynvarname into the context """
    print("CALLED"+str(dynvarname))
    return context.get("user_"+str(dynvarname), None)