from django.urls import path, register_converter

from . import views
from .converters import CategoryConverter

register_converter(CategoryConverter, 'category')

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='category-list'),
    path('<str:slug>/', views.category_detail, name='category-detail'),
    # path('<category:category>/', views.category_test, name='category-detail'),
]
