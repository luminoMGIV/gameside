from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='category-list'),
    path('<str:slug>/', views.category_detail, name='category-detail'),
]
