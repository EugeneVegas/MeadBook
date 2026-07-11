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
]
