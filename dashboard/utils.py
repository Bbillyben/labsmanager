
from datetime import datetime
from dateutil.relativedelta import relativedelta
from settings.models import LMUserSetting


def getDashboardTimeSlot(request):
    if not request.user:
        return {}
    
    pastMonth = LMUserSetting.get_setting('DASHBOARD_FUND_STALE_FROM_MONTH',user=request.user)
    nextMonth= LMUserSetting.get_setting('DASHBOARD_FUND_STALE_TO_MONTH',user=request.user)
    now = datetime.now()
    slot={}
    if pastMonth:
        slot["from"] =now + relativedelta(months=-pastMonth)
    if nextMonth and nextMonth > 0:
        slot["to"]=now + relativedelta(months=+nextMonth)
    
    return slot

def getDashboardMilestonesTimeSlot(request):
    if not request.user:
        return {}
    
    pastMonth = LMUserSetting.get_setting('DASHBOARD_MILESTONES_STALE_FROM_MONTH',user=request.user)
    nextMonth= LMUserSetting.get_setting('DASHBOARD_MILESTONES_STALE_TO_MONTH',user=request.user)
    now = datetime.now()
    slot={}
    if pastMonth:
        slot["from"] =now + relativedelta(months=-pastMonth)
    if nextMonth and nextMonth > 0:
        slot["to"]=now + relativedelta(months=+nextMonth)
    
    return slot    

def getDateToStale(monthToGo):
    return datetime.now()+ relativedelta(months=+monthToGo)