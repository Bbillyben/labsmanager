from collections import OrderedDict
from typing import List

from django.http import JsonResponse
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_tables2 import Column, SingleTableMixin, Table

class TableViewMixin(SingleTableMixin):
    # disable pagination to retrieve all data
    # https://mattsch.com/2021/05/28/django-django_tables2-and-bootstrap-table/
    
    table_pagination = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # build list of columns and convert it to an
        # ordered dict to retain ordering of columns
        # the dict maps from column name to its header (verbose name)
        table: Table = self.get_table()
        table_columns: List[Column] = [
            column
            for column in table.columns
        ]

        # retain ordering of columns
        columns_tuples = [(column.name, column.header) for column in table_columns]
        columns: OrderedDict[str, str] = OrderedDict(columns_tuples)

        context['columns'] = columns

        return context

    def get(self, request, *args, **kwargs):
        # trigger filtering to update the resulting queryset
        # needed in case of additional filtering being done
        response = super().get(self, request, *args, **kwargs)
        
        if 'json' in request.GET:
            table: Table = self.get_table()

            data = [
                {column.name: cell for column, cell in row.items()}
                for row in table.paginated_rows
            ]

            return JsonResponse(data, safe=False)
        else:
            return response
        
        
        
class LabsManagerBudgetMixin(models.Model):
    class Meta:
        abstract = True
        
    amount=models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'), default=0, null=True)
    expense=models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Expense'), default=0, null=True)
    
    @property
    def available(self):
        return self.amount + self.expense
    
    def clean_expense(self):
        if self.cleaned_data['expense']>0:
            self.cleaned_data['expense']=-self.cleaned_data['expense']
        return self.cleaned_data['expense']