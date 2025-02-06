from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('<int:pk>/games/', views.order_game_list, name='order-games-list'),
    path('<int:pk>/confirm/', views.confirm_order, name='confirm-order'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:pk>/pay/', views.pay_order, name='pay-order'),
]
