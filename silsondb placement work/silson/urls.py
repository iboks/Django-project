from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from .models import Staff
from .models import Customer
from .models import Affiliation
from .models import User
from . import views
from .views import CustomerListing, CustomerDetail, CustomerCreate, CustomerUpdate, CustomerFilter
from .views import StaffListing, StaffDetail, StaffUpdate, StaffCreate, StaffDelete, StaffFilter
from .views import UserListing, UserDetail, UserUpdate, UserCreate, UserFilter
from .views import AffiliationListing, AffiliationDetail, AffiliationUpdate, AffiliationCreate, AffiliationFilter
from django_filters.views import FilterView

app_name = 'silson'

urlpatterns = [
    
   url(r'^$', views.home),
   url(r'^staff/$', StaffListing.as_view(), name ='staff_list'),
    url(r'^staff/create/$',StaffCreate.as_view(), name ='create'),
    url(r'^staff/(?P<pk>\d+)/$',StaffDetail.as_view(), name ='staff_detail'),
    url(r'^staff/search/$', views.staff_list),
    url(r'^staff/search/(?P<pk>\d+)/$',views.staff_search),    
     url(r'^staff/(?P<pk>\d+)/update/$', StaffUpdate.as_view(), name='update'),
    url(r'^staff/(?P<pk>\d+)/delete/$', StaffDelete.as_view(), name='delete'), 

    url(r'^customer/$', CustomerListing.as_view(), name ='customer_list'),
    url(r'^customer/create/$',CustomerCreate.as_view(), name ='create'), 
    url(r'^customer/search/$', views.customer_list),
    url(r'^customer/search/(?P<pk>\w+)/$',views.customer_search),
    url(r'^customer/(?P<pk>\w+)/$',CustomerDetail.as_view(), name ='customer_detail'),
    url(r'^customer/(?P<pk>\w+)/update/$', CustomerUpdate.as_view(), name='update'),  
    

    url(r'^affiliation/$', AffiliationListing.as_view(), name ='affiliation_list'),
    url(r'^affiliation/create/$',AffiliationCreate.as_view(), name ='create'),    
    url(r'^affiliation/(?P<pk>\d+)/$',AffiliationDetail.as_view(), name ='affiliation_detail'),
    url(r'^affiliation/(?P<pk>\d+)/update/$', AffiliationUpdate.as_view(), name='update'),
     url(r'^affiliation/search/$', views.affiliation_list),   
    url(r'^affiliation/search/(?P<pk>\d+)/$',views.affiliation_search), 

    url(r'^user/$', UserListing.as_view(), name ='user_list'),
    url(r'^user/create/$',UserCreate.as_view(), name ='create'),
    
     url(r'^user/(?P<pk>\d+)/$',UserDetail.as_view(), name ='user_detail'),
    url(r'^user/(?P<pk>\d+)/update/$', UserUpdate.as_view(), name='update'),     
     url(r'^user/search/$', views.user_list),
    url(r'^user/search/(?P<pk>\d+)/$',views.user_search),
     
]

