from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import loader, context
from django.http import HttpResponseRedirect,HttpResponse,HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Wafer
from .models import Mask
from .models import Process_record
from .models import Jobb
import datetime
import django_filters
from django.db.models import Q
from django.forms import inlineformset_factory
from .forms import Process_recordFormSet, JobbForm
class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
def home(request):
    return render(request, 'orders/home.html')
class MaskListing(ListView):
     model = Mask
class MaskCreate(CreateView):
    model = Mask
    success_url ='/jobs/mask'
    fields= ['reference','membrane_size','wafer_dia','wafer_thickness','number_available','frame_size','comment']
class MaskDetail(DetailView):
    model = Mask
class MaskUpdate(UpdateView):
    model = Mask
    fields= ['reference','membrane_size','wafer_dia','wafer_thickness','number_available','frame_size','comment']
    def get_success_url(self):
         return reverse('orders:mask_detail', kwargs={
             'pk': self.object.pk,
         })

class WaferListing(ListView):
     model = Wafer
class WaferCreate(CreateView):
    model = Wafer
    success_url ='/jobs/wafer'
    fields= ['reference','coating','coating_thickness','silicon_date','diameter','box_no','no_of_wafers','stress','polish','membrane_thickness','comment']
class WaferDetail(DetailView):
    model = Wafer
class WaferUpdate(UpdateView):
    model = Wafer
    fields= ['reference','coating','coating_thickness','silicon_date','diameter','box_no','no_of_wafers','stress','polish','membrane_thickness','comment']
    def get_success_url(self):
         return reverse('orders:wafer_detail', kwargs={
             'pk': self.object.pk,
         })
class JobbListing(ListView):
     model = Jobb
class JobbCreate(FormsetMixin,CreateView):
    model = Jobb
    success_url ='/jobs/job'
    form_class=JobbForm
    formset_class = Process_recordFormSet
    
    
class JobbDetail(DetailView):
    model = Jobb
class JobbUpdate(FormsetMixin,UpdateView):
    model = Jobb
    is_update_view =True
    form_class=JobbForm
    formset_class= Process_recordFormSet
    #fields= ['job_No','customer','p_order_no','p_order_date','po_acknowledged','ship_by','purchase_contact','end_user','date_received','disp_date','disp_advised','POD_Date','invoice_No','invoice_Date','payment_received','comments']
    def get_success_url(self):
         return reverse('orders:jobb_detail', kwargs={
             'pk': self.object.pk,
         })
class JobbFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(lookup_expr='icontains')
    purchase_contact = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Jobb
        fields = ['customer','purchase_contact']

def jobb_list(request):
    query = request.GET['q']
    f = JobbFilter(request.GET, 
      queryset=Jobb.objects.all().filter(Q(customer__full_Name__icontains= query)|Q(purchase_contact__name__icontains=query)).distinct())
    return render(request, 'orders/jobb_search.html',{'filter' :f})


def jobb_search(request,jobb_id):
   return render_to_response('jobb_detail.html',{'job':Jobb.objects.get(pk=jobb_id)}) 

class Process_recordListing(ListView):
     model = Process_record

class Process_recordCreate(CreateView):
    model = Process_record
    success_url ='/jobs/prs'
    fields= ['sheet_No','job_No','customer','job_Date','number_required','mask_ref','wafer_ref','membrane_thickness','frame_size','frame_added_to_stock','apertures','comment']
class Process_recordDetail(DetailView):
    model = Process_record
class Process_recordUpdate(UpdateView):
    model = Process_record
    fields= ['sheet_No','job_No','customer','job_Date','number_required','mask_ref','wafer_ref','membrane_thickness','frame_size','frame_added_to_stock','apertures','comment']
    def get_success_url(self):
         return reverse('orders:process_record_detail', kwargs={
             'pk': self.object.pk,
         })
class Process_recordFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Process_record
        fields = ['customer']

def process_record_list(request):
    query = request.GET['q']
    f = Process_recordFilter(request.GET, 
      queryset=Process_record.objects.all().filter(customer__full_Name__icontains= query).distinct())
    return render(request, 'orders/process_record_search.html',{'filter' :f})


def process_record_search(request,process_record_id):
   return render_to_response('process_record_detail.html',{'process_record':Process_record.objects.get(pk=process_record_id)}) 
