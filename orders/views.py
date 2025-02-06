from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.serializers import GameSerializer
from shared.decorators import json_check, method_check, user_check

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@method_check('POST')
@user_check
def add_order(request, user):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


@method_check('GET')
def order_game_list(request, pk):
    try:
        games = GameSerializer(Order.objects.get(pk=pk).games.all())
        return data.json_response()
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@method_check('POST')
@user_check
def order_detail(request, pk, user):
    try:
        order = Order.objects.get(pk=pk)
        if order.user == user:
            data = OrderSerializer(order)
            return data.json_response()
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@method_check('POST')
@user_check
def confirm_order(request, pk, user):
    try:
        order = Order.objects.get(pk=pk)
        if order.user == user:
            order.status = Order.status.PAID
            return JsonResponse({'status': order.get_status_display()}, status=200)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@method_check('POST')
@user_check
def cancel_order(request, pk, user):
    try:
        order = Order.objects.get(pk=pk)
        if order.user == user:
            order.status = Order.status.CANCELLED
            return JsonResponse({'status': order.get_status_display()}, status=200)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@method_check('POST')
@user_check
@json_check
def pay_order(request, pk, user, json_data):
    try:
        order = Order.objects.get(pk=pk)
        if order.user == user:
            if order.status == Order.status.CONFIRMED:
                pass
            return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
