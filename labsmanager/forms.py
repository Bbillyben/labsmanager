from django.forms import DateInput

class DateInput(DateInput):
    input_type = 'date'
    
    def __init__(self, attrs=None, format=None):
        super().__init__(attrs)
        self.format = format or None
        
    def format_value(self, value):
        return value
        # return formats.localize_input(
        #     value, self.format or formats.get_format(self.format_key)[0]
        # )