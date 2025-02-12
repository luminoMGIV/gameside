from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import card_check, json_check, method_check, order_check, user_check

from .models import Order
from .serializers import OrderSerializer

# @csrf_exempt
# @method_check
# @user_check
# def add_order(request, user, method):
#     order = Order.objects.create(user=user)
#     return JsonResponse({'id': order.pk}, status=200)


# @method_check
# @user_check
# @order_check
# def order_game_list(request, pk, user, order, method):
#     data = GameSerializer(order.games.all())
#     return data.json_response()


# @csrf_exempt
# @method_check
# @json_check
# @user_check
# @order_check
# def add_game_to_order(request, pk, user, json_data, order, method):
#     game = Game.objects.get(slug=json_data['game-slug'])
#     game.stock -= 1
#     game.save()
#     order.games.add(game)
#     return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


# @method_check
# @user_check
# @order_check
# def order_detail(request, pk, user, order, method):
#     data = OrderSerializer(order)
#     return data.json_response()


# @method_check
# @json_check
# @user_check
# @order_check
# # ⊛ Al cancelar un pedido se debe actualizar el stock de los juegos añadidos al pedido.
# def change_order_status(request, pk, user, json_data, order, method):
#     if not Order.check_status(
#         (new_status := json_data['status']), [Order.Status.CONFIRMED, Order.Status.CANCELLED]
#     ):
#         return JsonResponse({'error': 'Invalid status'}, status=400)

#     if Order.check_status(order.status, [Order.Status.INITIATED]):
#         order.status = new_status
#         order.save()
#         return JsonResponse({'status': order.get_status_display()}, status=200)
#     return JsonResponse(
#         {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
#     )


# @method_check
# @json_check
# @user_check
# @order_check
# @card_check
# def pay_order(request, pk, user, json_data, order, method, fields):
#     if Order.check_status(order.status, [Order.Status.CONFIRMED]):
#         order.status = Order.Status.PAID
#         order.save()
#         return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)
#     return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)


@csrf_exempt
@method_check
@user_check
def add_order(request, user, method):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


@method_check
@user_check
@order_check
def order_game_list(request, user, order, method):
    data = GameSerializer(order.games.all())
    return data.json_response()


@csrf_exempt
@method_check
@json_check
@user_check
@order_check
def add_game_to_order(request, user, json_data, order, method, fields):
    game = Game.objects.get(slug=json_data['game-slug'])
    game.stock -= 1
    game.save()
    order.games.add(game)
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


@method_check
@user_check
@order_check
def order_detail(request, user, order, method):
    data = OrderSerializer(order)
    return data.json_response()


@method_check
@json_check
@user_check
@order_check
# ⊛ Al cancelar un pedido se debe actualizar el stock de los juegos añadidos al pedido.
def change_order_status(request, user, json_data, order, method, fields):
    if not Order.check_status(
        (new_status := json_data['status']), [Order.Status.CONFIRMED, Order.Status.CANCELLED]
    ):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    if Order.check_status(order.status, [Order.Status.INITIATED]):
        order.status = new_status
        order.save()
        return JsonResponse({'status': order.get_status_display()}, status=200)
    return JsonResponse(
        {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
    )


@method_check
@json_check
@user_check
@order_check
@card_check
def pay_order(request, user, json_data, order, method, fields):
    if Order.check_status(order.status, [Order.Status.CONFIRMED]):
        order.status = Order.Status.PAID
        order.save()
        return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)
    return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
