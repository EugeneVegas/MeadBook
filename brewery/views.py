from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Batch, Measurement

from .forms import BatchForm, MeasurementForm

from .utils import qr


class BatchLabelView(DetailView):
    model = Batch
    template_name = 'brewery/batch/label.html'
    context_object_name = 'batch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batch = self.get_object()
        absolute_url = reverse_lazy('batch_detail', kwargs={'pk': batch.pk},)
        context['qr_code'] = qr.make_qr(
            self.request.build_absolute_uri(absolute_url))

        return context


class BatchListView(ListView):
    model = Batch
    template_name = 'brewery/batch/list.html'
    context_object_name = 'batches'


class BatchDetailView(DetailView):
    model = Batch
    template_name = 'brewery/batch/detail.html'
    context_object_name = 'batch'


class BatchCreateView(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'brewery/batch/form.html'
    success_url = reverse_lazy('batch_list')


class BatchUpdateView(UpdateView):
    model = Batch
    form_class = BatchForm
    template_name = 'brewery/batch/form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('batch_detail',
                            kwargs={'pk': self.object.pk})


class MeasurementSuccessUrlMixin:
    def get_success_url(self) -> str:
        return reverse_lazy('batch_detail',
                            kwargs={'pk': self.object.batch.pk})


class MeasurementCreateView(MeasurementSuccessUrlMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'brewery/measurement/form.html'

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


class MeasurementUpdateView(MeasurementSuccessUrlMixin, UpdateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'brewery/measurement/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.object.batch
        return context


class MeasurementDeleteView(DeleteView):
    model = Measurement
    template_name = 'brewery/measurement/confirm_delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('batch_detail',
                            kwargs={'pk': self.object.batch.pk})


class MeasurementListView(ListView):
    model = Measurement
    template_name = 'brewery/measurement/list.html'
    context_object_name = 'measurements'

    def get_queryset(self):
        return get_object_or_404(
            Batch,
            pk=self.kwargs['pk'],
        ).measurements.all()

    def get_batch(self):
        return get_object_or_404(
            Batch,
            pk=self.kwargs['pk'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batch'] = self.get_batch()
        return context
