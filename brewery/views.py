from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from .models import Batch, Measurement

from .forms import BatchForm, MeasurementForm


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


class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'brewery/measurement_form.html'

    def get_batch(self):
        return get_object_or_404(
            Batch,
            pk=self.kwargs['pk'],
        )

    def form_valid(self, form):
        form.instance.batch = self.get_batch()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.get_batch()
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('batch_detail',
                            kwargs={'pk': self.object.batch.pk})
