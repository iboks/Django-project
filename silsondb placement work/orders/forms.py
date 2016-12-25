from django.forms import ModelForm


from django.forms import inlineformset_factory

from .models import Jobb, Process_record


class JobbForm(ModelForm):
    class Meta:
        model = Jobb
        fields='__all__'
        
class Process_recordForm(ModelForm):
    class Meta:
        model = Process_record
        fields='__all__'
Process_recordFormSet = inlineformset_factory(Jobb, Process_record, extra=0, min_num=1, fields=('__all__'))
