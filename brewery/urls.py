from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("batch/new/", views.batch_create, name="batch_create"),
]
