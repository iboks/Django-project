from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime
from django_countries.fields import CountryField
from localflavor.us.models import USStateField
from internationalflavor.vat_number import VATNumberField
from simple_history.models import HistoricalRecords

class Staff(models.Model):
    name = models.CharField(max_length=20)
    telephone = models.CharField(max_length=14, blank=True)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length= 120 ,blank =True)
    def __str__(self):
        return self.name
  
class Customer(models.Model):
    account_ID = models.CharField(max_length=16, primary_key=True, unique=True)
    full_Name = models.CharField(max_length=96, blank =True)
    acronym = models.CharField(max_length=32, blank = True)
    website = models.URLField(blank = True)
    address = models.CharField(max_length= 100)
    telephone = models.CharField(max_length=16,blank = True)
    country = CountryField(blank_label='(select country)')
    
    state = models.CharField(max_length=30,blank = True)
    us_state = USStateField(blank=True)
  
    VAT = VATNumberField(blank=True,null= False)
    date_added = models.DateField()
    added_by =models.ForeignKey(Staff, on_delete=models.CASCADE, null = True)
    type_Of_Customer=(('Gov','Government'),('Edu','Education'),('Co','Corporation'),('Ind','Individual'),('Pri','Private'))
    customer_type = models.CharField(max_length=3, choices=type_Of_Customer,blank = False,null=False)
    stat=(('V','Valid'),('I','Invalid'))
    status=models.CharField(max_length=8,choices=stat)
    associate= models.ManyToManyField(
        User,
        through='Affiliation',
        through_fields=('associate', 'name'),)
    history = HistoricalRecords()
    def save(self, force_insert=False, force_update=False):
        self.account_ID =self.account_ID.upper()
        super(Customer, self).save(force_insert, force_update)
    def __str__(self):
        return self.account_ID

class Affiliation(models.Model): 
    name = models.ForeignKey(User,on_delete = models.CASCADE)
    associate = models.ForeignKey(Customer, on_delete = models.CASCADE)    
    role = models.CharField(max_length=20)
    start = models.DateField()
    end = models.DateField(blank=True,null = True)
    comments =models.TextField(blank=True)
    history = HistoricalRecords()
    def __str__(self):
       return self.name.name    




