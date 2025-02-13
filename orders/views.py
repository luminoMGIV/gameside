from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import card_check, json_check, method_check, order_check, user_check

from .models import Order
from .serializers import OrderSerializer

@csrf_exempt
@method_check
@user_check
def add_order(request, user, method):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


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
def add_game_to_order(request, pk, user, json_data, order, method, fields):
    game = Game.objects.get(slug=json_data['game-slug'])
    game.stock -= 1
    game.save()
    order.games.add(game)
    order.save()
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


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
    order.status = new_status
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)

@csrf_exempt
@method_check
@json_check
@user_check
@order_check
@card_check
def pay_order(request, pk, user, json_data, order, method, fields, status, msg):
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)
