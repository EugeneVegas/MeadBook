from django.urls import path

from . import views

urlpatterns = [
    path('', views.BatchListView.as_view(), name='batch_list'),
    path('batch/<int:pk>/', views.BatchDetailView.as_view(),
         name='batch_detail'),
    path('batch/new/', views.BatchCreateView.as_view(), name='batch_create'),
    path('batch/<int:pk>/measurements/new/',
         views.MeasurementCreateView.as_view(),
         name='measurement_create'),
    path('measurement/<int:pk>/edit/',
         views.MeasurementUpdateView.as_view(),
         name='measurement_update'),
    path('measurement/<int:pk>/delete/',
         views.MeasurementDeleteView.as_view(),
         name='measurement_delete'),
    path('batch/<int:pk>/measurements/',
         views.MeasurementListView.as_view(),
         name='measurement_list'),
    path('batch/<int:pk>/label/',
         views.BatchLabelView.as_view(),
         name='batch_label'),
    path('batch/<int:pk>/edit/', views.BatchUpdateView.as_view(),
         name='batch_update'),
]
