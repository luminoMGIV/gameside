from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.serializers import GameSerializer
from shared.decorators import *

from .models import Order
from .serializers import OrderSerializer

@csrf_exempt
@method_check
@user_check
def add_order(request, user, method):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk})


@method_check
@user_check
@order_check
def order_game_list(request, pk, user, order, method):
    data = GameSerializer(order.games.all())
    return data.json_response()


@csrf_exempt
@method_check
@json_check
@user_check
@order_check
def add_game_to_order(request, pk, user, json_data, order, method, fields, game):
    order.add_game(game)
    return JsonResponse({'num-games-in-order': order.games.count()})


@method_check
@user_check
@order_check
def order_detail(request, pk, user, order, method):
    data = OrderSerializer(order)
    return data.json_response()

@csrf_exempt
@method_check
@json_check
@user_check
@order_check
def change_order_status(request, pk, user, json_data, order, method, fields, status, msg):
    if (new_status := json_data['status']) not in (Order.Status.CONFIRMED, Order.Status.CANCELLED):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    order.change_status(new_status)
    return JsonResponse({'status': order.get_status_display()})

@csrf_exempt
@method_check
@json_check
@user_check
@order_check
@card_check
def pay_order(request, pk, user, json_data, order, method, fields, status, msg):
    order.change_status(Order.Status.PAID)
    return JsonResponse({'status': order.get_status_display(), 'key': order.key})
