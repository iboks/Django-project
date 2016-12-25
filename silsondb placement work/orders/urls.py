from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from . import views
from .models import Mask
from .models import Wafer
from .models import Process_record
from .models import Jobb
from .views import WaferListing, WaferDetail, WaferCreate, WaferUpdate
from .views import MaskListing, MaskDetail, MaskCreate, MaskUpdate
from .views import Process_recordListing, Process_recordDetail, Process_recordCreate, Process_recordUpdate
from .views import JobbListing, JobbDetail, JobbCreate, JobbUpdate
app_name = 'orders'
urlpatterns = [
    
   url(r'^$', views.home),
   url(r'^wafer/$', WaferListing.as_view(), name ='wafer_list'),
    url(r'^wafer/create/$',WaferCreate.as_view(), name ='create'),
    url(r'^wafer/(?P<pk>\d+)/$',WaferDetail.as_view(), name ='wafer_detail'),
     url(r'^wafer/(?P<pk>\d+)/update/$', WaferUpdate.as_view(), name='update'),

    url(r'^mask/$', MaskListing.as_view(), name ='mask_list'),
    url(r'^mask/create/$',MaskCreate.as_view(), name ='create'), 
    url(r'^mask/(?P<pk>\d+)/$',MaskDetail.as_view(), name ='mask_detail'),
    url(r'^mask/(?P<pk>\d+)/update/$', MaskUpdate.as_view(), name='update'),  
    
    url(r'^job/$', JobbListing.as_view(), name ='jobb_list'),
    url(r'^job/create/$',JobbCreate.as_view(), name ='create'), 
    url(r'^job/(?P<pk>\d+)/$',JobbDetail.as_view(), name ='jobb_detail'),
    url(r'^job/(?P<pk>\d+)/update/$', JobbUpdate.as_view(), name='update'), 
     url(r'^job/search/$', views.jobb_list),
    url(r'^job/search/(?P<pk>\d+)/$',views.jobb_search),
     	
    url(r'^select2/', include('django_select2.urls')),

    url(r'^prs/$', Process_recordListing.as_view(), name ='process_record_list'),
    url(r'^prs/create/$',Process_recordCreate.as_view(), name ='create'),    
    url(r'^prs/(?P<pk>\d+)/$',Process_recordDetail.as_view(), name ='process_record_detail'),
    url(r'^prs/(?P<pk>\d+)/update/$', Process_recordUpdate.as_view(), name='update'),
     url(r'^prs/search/$', views.process_record_list),   
   url(r'^prs/search/(?P<pk>\d+)/$',views.process_record_search), 
]
