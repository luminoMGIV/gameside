from django.urls import path

from . import views

app_name = 'plaforms'

urlpatterns = [
    path('', views.platform_list, {'method': 'GET'}, name='platform-list'),
    path('<str:slug>/', views.platform_detail, {'method': 'GET'}, name='platform-detail'),
]
