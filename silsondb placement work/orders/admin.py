from django.contrib import admin
from .models import Wafer,Process_record, Mask, Jobb
from django import forms


class Process_recordInline(admin.StackedInline):
    model = Process_record
    extra = 1



# Register your models here.
class MaskAdminForm(forms.ModelForm):
    class Meta:
        model= Mask
        fields = ["reference"]
    def clean_name(self):
        return self.clean_name["reference"].upper()

class JobbAdmin(admin.ModelAdmin):
    fieldsets = [('Job Details', {'fields':['job_No','customer']}),('Customer Information', {'fields':['p_order_no','p_order_date','po_acknowledged','ship_by','purchase_contact','end_user']}), ('Other Information', {'fields':['date_received','disp_date','disp_advised','POD_Date','invoice_No','invoice_Date','payment_received','comments']})
]
    inlines = [Process_recordInline]
    list_filter = ['date_received','p_order_date',]
    search_fields = ['customer__full_Name']
    list_display = ('job_No', 'customer','p_order_date','ship_by','comments')
  

admin.site.register(Wafer)
admin.site.register(Mask)
admin.site.register(Process_record)
admin.site.register(Jobb,JobbAdmin)
