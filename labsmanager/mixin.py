from collections import OrderedDict
from typing import List

from django.http import JsonResponse

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
            print("====================================================> IS JSON")
            print(self.get_table())
            table: Table = self.get_table()

            data = [
                {column.name: cell for column, cell in row.items()}
                for row in table.paginated_rows
            ]

            return JsonResponse(data, safe=False)
        else:
            return response