from fund.models import Fund, Fund_Item
from fund.apps import FundConfig
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from expense.apps import ExpenseConfig

@receiver(post_save, sender=Fund_Item)
def save_Fund_Item_handler(sender, instance, **kwargs):
    print('[save_Fund_Item_handler] called')
    # print('  - sender :'+str(sender))    
    # print('  - instance :'+str(instance))
    # print('         - instance.fund :'+str(instance.fund))
    # print('         - instance.type :'+str(instance.type))
    # print('         - instance.amount :'+str(instance.amount))
    # print('         - instance.expense :'+str(instance.expense))
    # print('  - kwargs :'+str(kwargs))
    instance.fund.calculate()
    
@receiver(post_migrate)
def update_all_fund(sender, **kwargs):
    print('Receiver - post_migrate : update_all_fund :'+str(sender))
    # print(' - kwargs:'+str(kwargs))
    if type(sender) == FundConfig:
        fu=Fund.objects.all()
        for f in fu:
            f.calculate()
    