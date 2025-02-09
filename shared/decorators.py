import json
import re
from datetime import datetime, date

from django.http import JsonResponse
from users.models import Token
from games.models import Game
from orders.models import Order


def method_check(method):
    def inner_func(func):
        def wrapper(*args, **kwargs):
            if args[0].method == method:
                return func(*args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        return wrapper
    return inner_func

def user_check(func):
    def wrapper(*args, **kwargs):
        pattern = r'^Bearer ([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'
        match = re.match(pattern, args[0].headers.get('Authorization'))
        if match:
            token = match.group(1)
            try:
                user = Token.objects.get(key=token).user
                return func(user=user, *args, **kwargs)
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    return wrapper


def order_check(func):
    def wrapper(*args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['pk'])
            if func.__name__ == 'add_game_to_order':
                game = Game.objects.get(slug=kwargs['json_data']['game-slug'])
            if kwargs['user'] != order.user:
                return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
            return func(order=order, *args, **kwargs)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

    return wrapper


def json_check(fields):
    def inner_func(func):
        def wrapper(*args, **kwargs):
            try:
                json_data = json.loads(args[0].body)
                for field in fields:
                    if not json_data.get(field, None):
                        return JsonResponse({'error': 'Missing required fields'}, status=400)
                return func(json_data=json_data, *args, **kwargs)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        return wrapper
    return inner_func

def card_check(func):
    def wrapper(*args, **kwargs):
        card_data = kwargs['json_data']
        if not re.fullmatch(r'^\d{4}-\d{4}-\d{4}-\d{4}$', card_data['card-number']):
            return JsonResponse({'error': 'Invalid card number'}, status=400)
        if not re.fullmatch(r'^\d{3}$', card_data['cvc']):
            return JsonResponse({'error': 'Invalid CVC'}, status=400)
        if not re.fullmatch(r'^(0?[1-9]|1[0-2])\/\d{4}$', (card_date:= card_data['exp-date'])):
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)
        exp_date = datetime.strptime(card_date, "%m/%Y").date()
        if exp_date < date.today():
            return JsonResponse({'error': 'Card expired'}, status=400)
        return func(*args, **kwargs)

    return wrapper
