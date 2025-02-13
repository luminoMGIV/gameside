from django.urls import path

from . import views
from .models import Order

app_name = 'orders'


urlpatterns = [
    path('add/', views.add_order, {'method': 'POST'}, name='add-order'),
    path('<int:pk>/', views.order_detail, {'method': 'GET'}, name='order-detail'),
    path(
        '<int:pk>/status/',
        views.change_order_status,
        {'method': 'POST', 
         'fields': ['status'], 
         'status': Order.Status.INITIATED, 
         'msg':'Orders can only be confirmed/cancelled when initiated'},
        name='change-order-status',
    ),
    path(
        '<int:pk>/pay/',
        views.pay_order,
        {'method': 'POST', 'fields': ['card-number', 'exp-date', 'cvc'], 
         'status': Order.Status.CONFIRMED,
         'msg': 'Orders can only be paid when confirmed'},
        name='pay-order',
    ),
    path('<int:pk>/games/', views.order_game_list, {'method': 'GET'}, name='order-games-list'),
    path(
        '<int:pk>/games/add/',
        views.add_game_to_order,
        {'method': 'POST', 'fields': ['game-slug']},
        name='add-game-to-order',
    ),
]