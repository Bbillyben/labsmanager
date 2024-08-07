from import_export.resources import ModelResource
from import_export import results, widgets
from import_export.fields import Field
import datetime

from decimal import Decimal
from django.utils.encoding import force_str, smart_str
# ressource for import export 
class SimpleError(results.Error):
    def __init__(self, error, traceback=None, row=None):
        super().__init__(error, traceback=traceback, row=row)
        self.traceback = "redacted"
        
class labResource(ModelResource):
    """Custom subclass of the ModelResource class provided by django-import-export"
    Ensures that exported data are escaped to prevent malicious formula injection.
    Ref: https://owasp.org/www-community/attacks/CSV_Injection
    """

    def export_resource(self, obj):
        """Custom function to override default row export behaviour.
        Specifically, strip illegal leading characters to prevent formula injection
        """
        row = super().export_resource(obj)

        illegal_start_vals = ['@', '=', '+', '-', '@', '\t', '\r', '\n']

        for idx, val in enumerate(row):
            if type(val) is str:
                val = val.strip()

                # If the value starts with certain 'suspicious' values, remove it!
                while len(val) > 0 and val[0] in illegal_start_vals:
                    # Remove the first character
                    val = val[1:]

                row[idx] = val

        return row
    
class SkipErrorRessource(ModelResource):
    
    report_error_column=False
    
    def get_field_column_names(self):
        names = []
        for field in self.get_fields():
            names.append(field.column_name)
        return names

    def import_row(self, row, instance_loader, **kwargs):
        import_result = super(SkipErrorRessource, self).import_row(
            row, instance_loader, **kwargs
        )

        if import_result.import_type == results.RowResult.IMPORT_TYPE_ERROR:
            import_result.diff=[]
            for field in self.get_fields():
                import_result.diff.append(row.get(field.column_name, ''))
            
            if self.report_error_column:
                for row_name in row:
                    if not row_name in self.get_field_column_names():
                        import_result.diff.append(row.get(row_name, ''))

            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = results.RowResult.IMPORT_TYPE_SKIP

        return import_result
    
    class Meta:
        abstract = True
        
        
################################ Field COMMON #################################    

class DateField(Field):
        
    def get_value(self, obj):
        val=super().get_value(obj)
        if isinstance(val, datetime.datetime):
            return val.date()
        return val   
    
class DecimalField(Field):
    def clean(self, data, **kwargs):
        ''' Force Value 0 if not set
        '''
        if data[self.column_name] is None:
            data[self.column_name]= 0
        
        return super().clean(data, **kwargs)
    
    
################################ WIDGETS COMMON #################################
from staff.models import Employee
class EmployeeWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        #emp=Employee.objects.get(pk=value)
        return value.__str__()

class FundWidget(widgets.CharWidget):
    
    def render(self, value, obj=None):
        strC= str(value.funder.short_name) 
        strC+= " - " +str(value.institution.short_name)
        strC+='('+str(value.ref)
        strC+=' - '+str(value.amount)+")"
       
        return strC  

class percentageWidget(widgets.DecimalWidget):
    max_num=4
    def __init__(self, max_num=False):
        self.max_num = max_num
    
    def render (self, value, obj=None,  **kwargs):
        #val=super().render(value, obj)
        try:
            val = round(value*100, self.max_num)
            val = str(val)+"%"
        except:
            val="-"            
        return val

class InfoWidget(widgets.CharWidget):
    def render(self, value, obj=None):
        li=[]
        for c in value:
            strC= str(c.info.name) 
            strC+= " : " +str(c.value)
            li.append(strC)
        return "\n".join(li)
    
class ContenTypeObjectWidget(Field):
    fieldnames="name"
    def __init__(self, fieldnames=False):
        self.fieldnames = fieldnames
    
    def render (self, value, obj=None,  **kwargs):
        md_class=obj.content_type.model_class()
        # print("[ContenTypeObjectWidget]")
        # print(f" Id : {obj.id}  / class :{md_class} / obj id:{obj.object_id}")
        ob=md_class.objects.get(pk = obj.object_id)
        attrs = self.fieldnames.split("__")
        val=ob
        for x in attrs:
            val= getattr(val, x)
            if not val:
                return None
        if val is not None:
            return val
                
        return None