from django.contrib import admin
from .models import Staff
from .models import Affiliation
from .models import Customer
from .models import User
from django import forms
from easy_select2 import select2_modelform

CustomerForm = select2_modelform(Customer, attrs={'width':'200px'})
class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields = ["account_ID"]
    def clean_name(self):
        return self.clean_name["account_ID"].upper()


class CustomerAdmin(admin.ModelAdmin):
    form =CustomerForm
    fieldsets = [('Customer Information', {'fields':['account_ID','full_Name','acronym']}),('Contact Detail', {'fields':['address','country','state','us_state','telephone','website']}), ('Additional Information', {'fields':['VAT','customer_type','date_added','status','added_by']})
]
    
    list_filter = ['date_added','status','customer_type',]
    search_fields = ['full_Name','acronym']
    list_display = ('account_ID', 'full_Name','acronym','address','country','status','date_added')
  
 


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Affiliation)
admin.site.register(Staff)
admin.site.register(User)


