import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import method_check, user_check
from games.serializers import GameSerializer

from .models import Order
from .serializers import OrderSerializer

@csrf_exempt
@method_check('POST')
@user_check
def add_order(request, user):
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk }, status=200)


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
            order = Order.objects.get(pk=pk)
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
            order = Order.objects.get(pk=pk)
            order.status = Order.status.CANCELLED
            return JsonResponse({'status': order.get_status_display()}, status=200) 
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@method_check('POST')
def pay_order(request, pk):
    pass
