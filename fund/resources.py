from django.utils.translation import gettext as _
from django.db.models import Q
from labsmanager.ressources import labResource, SkipErrorRessource, percentageWidget
from .models import Fund_Item, Fund, Cost_Type, Budget
from import_export.fields import Field
from labsmanager.utils import getDateFilter
import import_export.widgets as widgets
from import_export.fields import Field


        
        
class FundItemResource(labResource):
    available=Field(
        column_name=_('Total Available'),
        attribute='available', 
        widget=widgets.DecimalWidget(), readonly=True
    )
    type=Field(
        column_name=_('type'),
        attribute='type', 
        widget=widgets.ForeignKeyWidget(Cost_Type, 'name'), readonly=True
    )
    project=Field(
        column_name=_('Project'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'project__name'), readonly=True
    )
    funder=Field(
        column_name=_('funder'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'funder__short_name'), readonly=True
    )
    institution=Field(
        column_name=_('institution'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'institution__short_name'), readonly=True
    )
    start_date=Field(
        column_name=_('Start Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'start_date'), readonly=False
    )
    end_date=Field(
        column_name=_('End Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'end_date'), readonly=False
    )
    fund=Field(
        column_name=_('Ref'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'ref'), readonly=True
    )
    
    class Meta:
        """Metaclass"""
        model = Fund_Item
        skip_unchanged = False
        clean_model_instances = False
        exclude = [ 'id','fund' ]
        export_order=['project', 
                      'funder',
                      'institution',
                      'start_date',
                      'end_date',
                      'type',
                      'fund',
                      'amount',
                      'expense',
                      'available',
                      ]
        

class FundItemField(Field):
     def clean(self, data, **kwargs):
        if data[self.column_name] is None:
            data[self.column_name]= 0
        
        return super().clean(data, **kwargs)

class FundField(Field):
     def clean(self, data, **kwargs):
        query = Q(amount__gte=-1)
        project_name = data.get('Project', None)
        if project_name is not None:
            query = query & Q(project__name__icontains=project_name)
        
        funder_name = data.get('funder', None)
        if funder_name is not None:
            query = query & (Q(funder__name__icontains=funder_name) | Q(funder__short_name__icontains=funder_name))
        
        inst_name = data.get('institution', None)
        if inst_name is not None:
            query = query & (Q(institution__name__icontains=inst_name) | Q(institution__short_name__icontains=inst_name))
        
        refI = data.get('Ref', None)
        if refI is not None:
            query = query & Q(ref=refI)
        
        fu = Fund.objects.filter(query).first()
        return fu
   
    
class FundItemAdminResource(labResource, SkipErrorRessource):
    fund=FundField(
        column_name=_('Ref'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'ref'), 
        readonly=False
    )
    type=Field(
        column_name=_('type'),
        attribute='type', 
        widget=widgets.ForeignKeyWidget(Cost_Type, 'short_name'), 
        readonly=False
    )
    project=FundField(
        column_name=_('Project'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'project__name'),
        readonly=False
    )
    funder=FundField(
        column_name=_('funder'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'funder__short_name'), 
        readonly=False
    )
    institution=FundField(
        column_name=_('institution'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'institution__short_name'), 
        readonly=False
    )
    start_date=FundField(
        column_name=_('Start Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'start_date'), 
        readonly=False
    )
    end_date=FundField(
        column_name=_('End Date'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'end_date'),
        readonly=False
    )
    
    amount=FundItemField(
        column_name=_('Budget'),
        attribute='amount', 
        widget=widgets.DecimalWidget(),
        readonly=False
    )
    expense=FundItemField(
        column_name=_('expense'),
        attribute='expense', 
        widget=widgets.DecimalWidget(),
        readonly=True
    )
    available=FundItemField(
        column_name=_('available'),
        attribute='available', 
        widget=widgets.DecimalWidget(),
        readonly=True
    )
            
        
    def before_import_row(self, row, row_number=None, **kwargs):
        query = Q(amount__gte=-1)
        project_name = row.get('Project', None)
        if project_name is not None:
            query = query & Q(fund__project__name__icontains=project_name)
        
        funder_name = row.get('funder', None)
        if funder_name is not None:
            query = query & (Q(fund__funder__name__icontains=funder_name) | Q(fund__funder__short_name__icontains=funder_name))
        
        inst_name = row.get('institution', None)
        if inst_name is not None:
            query = query & (Q(fund__institution__name__icontains=inst_name) | Q(fund__institution__short_name__icontains=inst_name))
        
        refI = row.get('Ref', None)
        if refI is not None:
            query = query & Q(fund__ref=refI)
            
        typeC = row.get('type', None)
        if typeC is not None:
            query = query & Q(type__short_name=typeC)            
        
        fu = Fund_Item.objects.filter(query).first()
        if fu is not None:
            row["id"] = fu.pk
        else:
            row["id"] = None
        return fu
        
    class Meta:
        """Metaclass"""
        model = Fund_Item
        skip_unchanged = True
        clean_model_instances = False
        exclude = [ '' ]
        #import_id_fields=('fund', 'type')
        export_order=['project', 
                      'funder',
                      'institution',
                      'start_date',
                      'end_date',
                      'type',
                      'fund',
                      'amount',
                      'expense',
                      'available',
                      ]
        
from staff.models import Employee_Type
from labsmanager.ressources import EmployeeWidget, FundWidget
from expense.models import Contract_type

class BudgetResource(labResource):
    
    cost_type=Field(
        column_name=_('Cost Type'),
        attribute='cost_type', 
        widget=widgets.ForeignKeyWidget(Cost_Type, 'name'), readonly=True
    )
    # fund=Field(
    #     column_name=_('Fund'),
    #     attribute='fund', 
    #     widget=FundWidget(), readonly=True
    # )
    funder=Field(
        column_name=_('Funder'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'funder__short_name'), readonly=True
    )
    institution=Field(
        column_name=_('Institution'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'institution__short_name'), readonly=True
    )
    ref=Field(
        column_name=_('Ref'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'ref'), readonly=True
    )
    emp_type=Field(
        column_name=_('Employee Type'),
        attribute='emp_type', 
        widget=widgets.ForeignKeyWidget(Employee_Type, 'name'), readonly=True
    )
    employee=Field(
        column_name=_('Employee'),
        attribute='employee', 
        widget=EmployeeWidget(), 
        readonly=True,
    )
    is_active=Field(
        column_name=_('Active'),
        attribute='fund', 
        widget=widgets.ForeignKeyWidget(Fund, 'is_active'), readonly=True
    )
    contract_type=Field(
        column_name=_('Contract Type'),
        attribute='contract_type', 
        widget=widgets.ManyToManyWidget(Contract_type,separator=', ',  field='name'), readonly=True
    )
    
    class Meta:
        """Metaclass"""
        model = Budget
        skip_unchanged = True
        clean_model_instances = False
        exclude = [ 'id', 'fund' ]
        # #import_id_fields=('fund', 'type')
        export_order=['cost_type', 
                      'funder',
                      'institution',
                      'ref',
                      'amount',
                      'emp_type',
                      'contract_type',
                      'employee',
                      'quotity',
                      'is_active',
                      ]
        

class FundConsumptionResource(labResource):
    project=Field(
        column_name=_('Project'),
        attribute='project', 
        widget=widgets.ForeignKeyWidget(Fund, 'name'), readonly=True
    )
    funder=FundField(
        column_name=_('funder'),
        attribute='funder', 
        widget=widgets.ForeignKeyWidget(Fund, 'short_name'), 
        readonly=False
    )
    institution=Field(
        column_name=_('institution'),
        attribute='institution', 
        widget=widgets.ForeignKeyWidget(Fund, 'short_name'), readonly=True
    )
    available=Field(
        column_name=_('available'),
        attribute='available', 
         widget=widgets.DecimalWidget(), readonly=True
    )
    consumption_ratio=Field(
        column_name=_('Consumption Ration'),
        attribute='get_consumption_ratio', 
         widget=percentageWidget(max_num=2), readonly=True
    )
    time_ratio=Field(
        column_name=_('Time Ratio'),
        attribute='get_time_ratio', 
        widget=percentageWidget(), readonly=True
    )

    class Meta:
        """Metaclass"""
        model = Fund
        skip_unchanged = False
        clean_model_instances = False
        exclude = [ 'id' ]
        export_order=['project', 
                      'funder',
                      'institution',
                      'ref',
                      'consumption_ratio',
                      'time_ratio',
                      'start_date',
                      'end_date',
                      'amount',
                      'expense',
                      'available',
                      ]