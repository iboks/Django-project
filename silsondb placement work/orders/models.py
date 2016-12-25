from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from silson.models import Customer, User, Affiliation
import datetime

class Wafer(models.Model):
    reference=models.CharField(max_length=15)
    coating=models.CharField(max_length=12)
    coating_thickness=models.IntegerField(default=0)
    diameter=models.FloatField(default=0)
    silicon_date=models.DateField()
    box_no=models.IntegerField(default=0)
    no_of_wafers=models.IntegerField(default=0)
    stress=models.CharField(max_length=5)
    polish=models.CharField(max_length=8)
    wafer_thickness=models.IntegerField(default=0)
    membrane_thickness=models.IntegerField(default=0)
    comment=models.TextField(blank=True)

    def __str__(self):            
        return self.reference

class Mask(models.Model):
    reference=models.CharField(max_length=12)
    membrane_size=models.FloatField(max_length= 10)
    wafer_dia=models.IntegerField(default=0)
    wafer_thickness=models.IntegerField(default=0)
    number_available= models.IntegerField(default=0)
    frame_size=models.FloatField(default=0)
    comment=models.TextField(blank=True)
    def save(self, force_insert=False, force_update=False):
        self.reference =self.reference.upper()
        super(Mask, self).save(force_insert, force_update)
    def __str__(self):            
        return self.reference

class Jobb(models.Model):
    job_No= models.CharField(max_length= 10)
    customer=models.ForeignKey(Customer)
    p_order_no = models.CharField(max_length=10)
    p_order_date = models.DateField(blank=True)
    po_acknowledged = models.DateField(blank=True)
    ship_b=(('FedEx','FedEx'),('DHL', 'DHL'),('DPD', 'DPD'))
    ship_by=models.CharField(max_length=7,choices= ship_b)  
    purchase_contact= models.ForeignKey(User)
    end_user = models.CharField(max_length=12)
    date_received=models.DateField(blank=True)
    disp_date= models.DateField(blank=True)
    disp_advised=models.DateField(blank=True)
    POD_Date = models.DateField(blank=True)
    invoice_No =models.CharField(max_length=10, blank=True)
    invoice_Date=models.DateField(blank=True)
    payment_received=models.DateField(blank=True)
    comments=models.TextField(blank=True)
    def __str__(self):
        return self.job_No

class Process_record(models.Model):
    sheet_No=models.CharField(max_length=10)
    job_No= models.ForeignKey(Jobb)
    customer=models.ForeignKey(Customer)
    job_Date= models.DateField()
    number_required=models.IntegerField(default=0)
    mask_ref=models.ForeignKey(Mask)
    wafer_ref=models.ForeignKey(Wafer)
    membrane_thickness=models.IntegerField(default=0)
    frame_size=models.FloatField(default=0)
    frame_added_to_stock=models.IntegerField(default=0)    
    apertures=models.TextField(blank=True)
    comment=models.TextField(blank=True)
    def __str__(self):
        return self.sheet_No
# Create your models here.
