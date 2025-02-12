from django.urls import path, register_converter

from . import views
from .converters import CategoryConverter

register_converter(CategoryConverter, 'category')

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, {'method': 'GET'}, name='category-list'),
    path('<category:category>/', views.category_detail, {'method': 'GET'}, name='category-detail'),
]
