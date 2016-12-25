from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import loader, context
from .models import Staff
from .models import Customer
from .models import User
from .models import Affiliation
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import datetime
import django_filters
from django.db.models import Q

def home(request):
    return render(request, 'silson/home.html')

class StaffListing(ListView):
     model = Staff
class StaffCreate(CreateView):
    model = Staff
    success_url ='/staff'
    fields= ['name','telephone']
class StaffDetail(DetailView):
    model = Staff
class StaffUpdate(UpdateView):
    model = Staff
    fields= ['name','telephone']
    def get_success_url(self):
         return reverse('silson:staff_detail', kwargs={
             'pk': self.object.pk,
         })
class StaffDelete(DeleteView):
    model = Staff
    success_url = '/staff'

   
class StaffFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Staff
        fields = ['name']

def staff_list(request):
    query = request.GET['q']
    f = StaffFilter(request.GET, 
      queryset=Staff.objects.all().filter(name__icontains= query) )
    return render(request, 'silson/staff_search.html',{'filter' :f})


def staff_search(request,staff_id):
   return render_to_response('staff_detail.html',{'staff':Staff.objects.get(pk=staff_id)}) 

class CustomerDetail(DetailView):
    model = Customer
   
class CustomerListing(ListView):
     model = Customer

class CustomerCreate(CreateView):
    model = Customer
    success_url ='/customer'
    fields= ['account_ID','full_Name','acronym','address','country','state','us_state','telephone','website', 'VAT','customer_type','date_added','status','added_by']

class CustomerUpdate(UpdateView):
    model = Customer
    fields= ['account_ID','full_Name','acronym','address','country','state','us_state','telephone','website', 'VAT','customer_type','date_added','status','added_by']
    def get_success_url(self):
         return reverse('silson:customer_detail', kwargs={
             'pk': self.object.pk,
         })
class CustomerFilter(django_filters.FilterSet):
    full_Name = django_filters.CharFilter(lookup_expr='icontains')
    acronym = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')
    VAT = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['full_Name','acronym','country','VAT']

def customer_list(request):
    query = request.GET['q']
    f = CustomerFilter(request.GET, 
      queryset=Customer.objects.all().filter(Q(full_Name__icontains= query)|Q(country__icontains=query)|Q(acronym__icontains=query)|Q(VAT__icontains=query)).distinct() )
    return render(request, 'silson/customer_search.html',{'filter':f})

def customer_search(request,account_ID):
   return render_to_response('customer_detail.html',{'customer':Customer.objects.get(pk=account_ID)}) 
    
class UserListing(ListView):
     model = User
class UserCreate(CreateView):
    model = User
    success_url ='/user'
    fields= ['name','address']
class UserDetail(DetailView):
    model = User
class UserUpdate(UpdateView):
    model = User
    fields= ['name','address']
    def get_success_url(self):
         return reverse('silson:user_detail', kwargs={
             'pk': self.object.pk,
         })
class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['name']

def user_list(request):
    query = request.GET['q']
    f = UserFilter(request.GET, 
      queryset=User.objects.all().filter(name__icontains= query) )
    return render(request, 'silson/user_search.html',{'filter' :f})

def user_search(request,user_id):
   return render_to_response('user_detail.html',{'user':User.objects.get(pk=user_id)}) 

class AffiliationListing(ListView):
     model = Affiliation
class AffiliationCreate(CreateView):
    model = Affiliation
    success_url ='/affiliation'
    fields= ['name','associate','role','start','end','comments']
class AffiliationDetail(DetailView):
    model = Affiliation
    
class AffiliationUpdate(UpdateView):
    model = Affiliation
    fields= ['name','associate','role','start','end','comments']
    def get_success_url(self):
         return reverse('silson:affiliation_detail', kwargs={
             'pk': self.object.pk,
         })
class AffiliationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    associate = django_filters.CharFilter(lookup_expr='icontains')
    
   
    class Meta:
        model = Affiliation
        fields = ['name','associate']

def affiliation_list(request):
    query = request.GET['q']
    f = AffiliationFilter(request.GET, 
      queryset=Affiliation.objects.all().filter(Q(name__name__icontains= query)|Q(associate__full_Name__icontains=query)).distinct())
    return render(request, 'silson/affiliation_search.html',{'filter' :f})

def affiliation_search(request,affiliation_id):
   return render_to_response('affiliation_detail.html',{'affiliation':Affiliation.objects.get(pk=affiliation_id)}) 


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body> Hello!!! It is now %s.</body></html>" % now
    return HttpResponse(html)

