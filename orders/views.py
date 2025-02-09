from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import json_check, method_check, user_check, card_check, order_check

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@method_check('POST')
@user_check
def add_order(request, user):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


@method_check('GET')
@user_check
@order_check
def order_game_list(request, pk, user, order):
    data = GameSerializer(order.games.all())
    return data.json_response()


@csrf_exempt
@method_check('POST')
@json_check(['game-slug'])
@user_check
@order_check
def add_game_to_order(request, pk, user, json_data, order):
    game = Game.objects.get(slug=json_data['game-slug'])
    order.games.add(game)
    return JsonResponse({'num-games-in-order': order.games.all().count() }, status=200)

@method_check('GET')
@user_check
@order_check
def order_detail(request, pk, user, order):
    data = OrderSerializer(order)
    return data.json_response()


@method_check('POST')
@json_check(['status'])
@user_check
@order_check
def change_order_status(request, pk, user, json_data, order):
    if not Order.check_status((new_status:= json_data['status']), [Order.Status.CONFIRMED, Order.Status.CANCELLED]):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    if Order.check_status(order.status, [Order.Status.INITIATED]):
        order.status = new_status
        order.save()
        return JsonResponse({'status': order.get_status_display()}, status=200)
    return JsonResponse({'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400)


@method_check('POST')
@json_check(['card-number', 'exp-date', 'cvc'])
@user_check
@order_check
@card_check
def pay_order(request, pk, user, json_data, order):
    if Order.check_status(order.status, [Order.Status.CONFIRMED]):
        order.status = Order.Status.PAID
        order.save()
        return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)
    return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
