from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.simple_upload, name='upload'),
    path('success', views.success, name='success')
]
