from django.urls import path, register_converter

from . import views
from .converters import PlatformConverter

app_name = 'plaforms'

register_converter(PlatformConverter, 'platform')

urlpatterns = [
    path('', views.platform_list, {'method': 'GET'}, name='platform-list'),
    path('<str:slug>/', views.platform_detail, {'method': 'GET'}, name='platform-detail'),
]
