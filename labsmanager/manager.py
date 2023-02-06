from django.db import models
from django.db.models import Q, Max
from datetime import date
from collections.abc import Iterable

class date_manager(models.Manager):
    def timeframe(self, slots):
        query=Q()
        if 'from' in slots:
            query= query & Q(end_date__gte=slots["from"])
        if 'to' in slots:
            query= query & Q(end_date__lte=slots["to"])
        return self.get_queryset().filter(query)

class Current_date_Manager(date_manager):
    def get_queryset(self):
        cdate = date.today()
        query = (Q(start_date__lte=cdate) | Q(start_date=None)) & (Q(end_date__gte=cdate) | Q(end_date=None))
        
        return super().get_queryset().filter(query)
    
class outof_date_Manager(date_manager):
    def get_queryset(self):
        cdate = date.today()
        query = Q(start_date__gte=cdate) | Q(end_date__lte=cdate)
        
        return super().get_queryset().filter(query)
    
    
class LastInManager(models.Manager):
    
    def get_queryset(self, sel_fund=None):
        # print("---------> LastInManager - get_queryset :"+str(self.model))
        # print("  - sel_fund : "+str(sel_fund))
        queryset = super().get_queryset()
        if sel_fund is not None:
            # print(" type : "+str(type(sel_fund)))
            if isinstance(sel_fund, str):
                sel_fund=sel_fund.split(",")
                # print("  - trsf sel fund : "+str(sel_fund))
            elif isinstance(sel_fund, int):
                sel_fund=[sel_fund]
                
            try:
                queryset=queryset.filter(fund__in=sel_fund)
                # print("  - fund found : "+str(queryset.count()))
            except:
                queryset = None
                # print("  IN ERROR")
                pass
        if not queryset:
            return super().get_queryset().none()
        
        queryset =  queryset.values('fund', 'type').annotate(max_date=Max('value_date'))
        query=Q()
        for t in queryset:
            query |= (Q(fund=t["fund"]) & Q(type=t["type"]) & Q(value_date=t["max_date"]))
        
        return super().get_queryset().filter(query)
    
    def fund(self, sel_fund):
        return self.get_queryset(sel_fund)