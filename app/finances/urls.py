from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'', views.FinancesView)

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="finances/index.html")),
    path('upload/', TemplateView.as_view(template_name="finances/upload.html"), name='upload'),
    path('upload_file/', views.FinancesView.as_view({'post': 'upload_file'}), name='upload_file'),
    path('success/', views.FinancesView.as_view({'get': 'success'}), name='success'),
    path('list/', views.FinancesView.as_view({'get': 'list_finances'}), name='list')
]
