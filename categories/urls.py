from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, {'method': 'GET'}, name='category-list'),
    path('<str:slug>/', views.category_detail, {'method': 'GET'}, name='category-detail'),
]
