from django.urls import path

from . import views

urlpatterns = [
    path('', views.batch_list, name='batch_list'),
    path('batch/new/', views.batch_create, name='batch_create'),
]
