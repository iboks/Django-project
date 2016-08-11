# Models for the customer db.
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django_countries.fields import CountryField
from localflavor.us.models import USStateField
from internationalflavor.vat_number import VATNumberField

class Staff(models.Model):
    name = models.CharField(max_length=20)
    telephone = models.CharField(max_length=14)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=50)
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
    #v_A_T = models.CharField(max_length=16,blank=True)
    v_A_T = VATNumberField(blank=True,null= False)
    date_added = models.DateField()
    added_by =models.ForeignKey(Staff, on_delete=models.CASCADE, null = True)
    type_Of_Customer=(('Gov','Government'),('Edu','Education'),('Co','Corporation'),('Ind','Individual'),('Pri','Private'))
    customer_type = models.CharField(max_length=3, choices=type_Of_Customer,blank = False,null=False)
    stat=(('V','Valid'),('I','Invalid'))
    status=models.CharField(max_length=8,choices=stat)
    associate= models.ManyToManyField(
        User,
        through='Association',
        through_fields=('associate', 'name'),)
    def __str__(self):
        return self.account_ID

class Association(models.Model): 
    name = models.ForeignKey(User,on_delete = models.CASCADE)
    associate = models.ForeignKey(Customer, on_delete = models.CASCADE)    
    role = models.CharField(max_length=20)
    start = models.DateField()
    end = models.DateField(blank=True,null = True)
    comments=models.TextField(blank=True)
    def __str__(self):
       return self.role    


# Admin setup

from django.contrib import admin
from .models import Staff
from .models import Association
from .models import Customer
from .models import User



class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [('Customer Information', {'fields':['account_ID','full_Name','acronym']}),('Contact Detail', {'fields':['address','country','state','us_state','telephone','website']}), ('Additional Information', {'fields':['v_A_T','customer_type','date_added','status','added_by']})
]
    list_filter = ['date_added','status','customer_type',]
    search_fields = ['full_Name','acronym']
    list_display = ('account_ID', 'full_Name','acronym','address','country','status','date_added')
  
 


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Association)
admin.site.register(Staff)
admin.site.register(User)

# url patterns 
from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from .models import Staff
from .models import Customer
from .models import Association
from .models import User
from . import views
from .views import CustomerListing, CustomerDetail, CustomerCreate, CustomerUpdate
from .views import StaffListing, StaffDetail, StaffUpdate, StaffCreate, StaffDelete
from .views import UserListing, UserDetail, UserUpdate, UserCreate
from .views import AssociationListing, AssociationDetail, AssociationUpdate, AssociationCreate
app_name = 'lipsy'

urlpatterns = [
    
   url(r'^$', views.home),
   url(r'^staff/$', StaffListing.as_view(), name ='staff_list'),
   url(r'^customer/$', CustomerListing.as_view(), name ='customer_list'),
   url(r'^association/$', AssociationListing.as_view(), name ='association_list'),
    url(r'^user/$', UserListing.as_view(), name ='user_list'),
   url(r'^time/$' , views.current_datetime, name='current_datetime'),
    url(r'^staff/(?P<pk>\d+)/$',StaffDetail.as_view(), name ='staff_detail'),
    url(r'^customer/(?P<pk>\w+)/$',CustomerDetail.as_view(), name ='customer_detail'),
     url(r'^association/(?P<pk>\d+)/$',AssociationDetail.as_view(), name ='Association_detail'),
     url(r'^user/(?P<pk>\d+)/$',UserDetail.as_view(), name ='user_detail'),
    url(r'^staff/create/$',StaffCreate.as_view(), name ='create'),
    url(r'^customer/create/$',CustomerCreate.as_view(), name ='create'),
    url(r'^association/create/$',AssociationCreate.as_view(), name ='create'),
    url(r'^user/create/$',UserCreate.as_view(), name ='create'),
    url(r'^staff/(?P<pk>\d+)/update/$', StaffUpdate.as_view(), name='update'),
    url(r'^customer/(?P<pk>\w+)/update/$', CustomerUpdate.as_view(), name='update'),
    url(r'^association/(?P<pk>\d+)/update/$', AssociationUpdate.as_view(), name='update'),
    url(r'^user/(?P<pk>\d+)/update/$', UserUpdate.as_view(), name='update'),
   url(r'^staff/(?P<pk>\d+)/delete/$', StaffDelete.as_view(), name='delete'), 

]
# models genric views templates and others
customer list
{% extends "lipsy/base.html" %}
{% load static %}


{% block content %}
<h2>Customer</h2>


<a href="create" class="btn btn-primary btn-lg active" role="button">Create</a>
<ul>
{% for customer in customer_list %}
 <li><a href = "{{customer.account_ID}}" >{{customer.full_Name}}</a></li>
{% endfor %}

{% endblock %}

Customer create form
{% extends "lipsy/base.html" %}
 {% block content %}
       
        
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save" />
</form>

   {% endblock %}
   
customer details list 
{% extends "lipsy/base.html" %}
  {%load staticfiles %}
{% block content %}

<h4>Customer Information</h4>
<p>Account ID :{{customer.account_ID}}</p>
<p>Name:{{customer.full_Name}}</p>
<p>Acronym :{{customer.acronym}}</p>
<h4>Contact Detail</h4>
<p>Address:{{customer.address}}</p>
<p>Country :{{customer.country}}</p>
<p>State :{{customer.state}}</p>
<p>US State :{{customer.us_state}}</p>
<p>Telephone :{{customer.telephone}}</p>
<p>Website :{{customer.website}}</p>
<h4>Additional Information</h4>
<p>VAT :{{customer.v_A_T}}</p>
<p>Customer Type :{{customer.customer_type}}</p>
<p>Date Added :{{customer.date_added}}</p>
<p>Status :{{customer.status}}</p>
<p>Added By :{{customer.added_by}}</p>

 <a href="update" class="btn btn-primary btn-lg active" role="button">Update</a>
{% endblock %}

Staff view list
{% extends "lipsy/base.html" %}
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static ' lipsy/style.css' %}" />
<li><a color = green </a></li>
{% block content %}
<h2>Staff</h2>


<a href="create" class="btn btn-primary btn-lg active" role="button">Create</a>
<ul>
{% for staff in staff_list %}
 <li><a href = "{{staff.id}}" >{{staff.name}}</a></li>
{% endfor %}

{% endblock %}

staff details and create

{% extends "lipsy/base.html" %}
  {%load staticfiles %}
{% block content %}


<p>Name: {{ staff.name}}</p>
<p>Telephone: {{staff.telephone}}</p>

 <a href="update" class="btn btn-primary btn-lg active" role="button">Update</a>
 <a href="delete" class="btn btn-primary btn-lg active" role="button">Delete</a>
{% endblock %}


{% extends "lipsy/base.html" %}
 {% block content %}
       
        
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Save" />
</form>

   {% endblock %}
   
   staff delete
   
   <form action="" method="post">
     {% csrf_token %}
     <input type="submit">
 </form>

   
   
#views
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponseRedirect,HttpResponse 
from .models import Staff
from .models import Customer
from .models import User
from .models import Association
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import datetime




def home(request):
    return render(request, 'lipsy/home.html')

class StaffListing(ListView):
     model = Staff
class StaffCreate(CreateView):
    model = Staff
    success_url ='/'
    fields= ['name','telephone']
class StaffDetail(DetailView):
    model = Staff
class StaffUpdate(UpdateView):
    model = Staff
    fields= ['name','telephone']
    def get_success_url(self):
         return reverse('lipsy:staff_detail', kwargs={
             'pk': self.object.pk,
         })
         
class StaffDelete(DeleteView):
    model = Staff
    success_url = '/'
    
    
class CustomerListing(ListView):
     model = Customer
class CustomerCreate(CreateView):
    model = Customer
    success_url ='/'
    fields= ['account_ID','full_Name','acronym','address','country','state','us_state','telephone','website', 'v_A_T','customer_type','date_added','status','added_by']
class CustomerDetail(DetailView):
    model = Customer
    
class CustomerUpdate(UpdateView):
    model = Customer
    fields= ['account_ID','full_Name','acronym','address','country','state','us_state','telephone','website', 'v_A_T','customer_type','date_added','status','added_by']
    def get_success_url(self):
         return reverse('lipsy:customer_detail', kwargs={
             'pk': self.object.pk,
         })
    
class UserListing(ListView):
     model = User
class UserCreate(CreateView):
    model = User
    success_url ='/'
    fields= ['name']
class UserDetail(DetailView):
    model = User
class UserUpdate(UpdateView):
    model = User
    fields= ['name']
    def get_success_url(self):
         return reverse('lipsy:user_detail', kwargs={
             'pk': self.object.pk,
         })

class AssociationListing(ListView):
     model = Association
class AssociationCreate(CreateView):
    model = Association
    success_url ='/'
    fields= ['name','associate','role','start','end','comments']
class AssociationDetail(DetailView):
    model = Association
    
class AssociationUpdate(UpdateView):
    model = Association
    fields= ['name','associate','role','start','end','comments']
    def get_success_url(self):
         return reverse('lipsy:association_detail', kwargs={
             'pk': self.object.pk,
         })


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body> Hello!!! It is now %s.</body></html>" % now
    return HttpResponse(html)
def staff(request):
    return render(request, 'lipsy/staff.html', {'staffs':Staff.objects.all()})
def detail(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    return render(request, 'lipsy/result.html', {'staff': staff})



