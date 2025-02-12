from django.urls import path, register_converter

from . import views
from .converters import OrderConverter

app_name = 'orders'

register_converter(OrderConverter, 'order')

# urlpatterns = [
#     path('add/', views.add_order, {'method': 'POST'}, name='add-order'),
#     path('<int:pk>/', views.order_detail, {'method': 'GET'}, name='order-detail'),
#     path(
#         '<int:pk>/status/',
#         views.change_order_status,
#         {'method': 'POST', 'fields': ['status']},
#         name='change-order-status',
#     ),
#     path(
#         '<int:pk>/pay/',
#         views.pay_order,
#         {'method': 'POST', 'fields': ['card-number', 'exp-date', 'cvc']},
#         name='pay-order',
#     ),
#     path('<int:pk>/games/', views.order_game_list, {'method': 'GET'}, name='order-games-list'),
#     path(
#         '<int:pk>/games/add/',
#         views.add_game_to_order,
#         {'method': 'POST', 'fields': ['game-slug']},
#         name='add-game-to-order',
#     ),
# ]


urlpatterns = [
    path('add/', views.add_order, {'method': 'POST'}, name='add-order'),
    path('<order:order>/', views.order_detail, {'method': 'GET'}, name='order-detail'),
    path(
        '<order:order>/status/',
        views.change_order_status,
        {'method': 'POST', 'fields': ['status']},
        name='change-order-status',
    ),
    path(
        '<order:order>/pay/',
        views.pay_order,
        {'method': 'POST', 'fields': ['card-number', 'exp-date', 'cvc']},
        name='pay-order',
    ),
    path('<order:order>/games/', views.order_game_list, {'method': 'GET'}, name='order-games-list'),
    path(
        '<int:pk>/games/add/',
        views.add_game_to_order,
        {'method': 'POST', 'fields': ['game-slug']},
        name='add-game-to-order',
    ),
]
