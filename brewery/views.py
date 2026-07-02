from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import Batch

from .forms import BatchForm


class BatchListView(ListView):
    model = Batch
    template_name = 'brewery/batch_list.html'
    context_object_name = 'batches'


class BatchDetailView(DetailView):
    model = Batch
    template_name = 'brewery/batch_detail.html'
    context_object_name = 'batch'


class BatchCreateView(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'brewery/batch_form.html'
    success_url = reverse_lazy('batch_list')
