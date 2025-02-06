import json
import re

from django.http import JsonResponse
from users.models import Token


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
        match = re.match(pattern, args[0].headers.get('Authorization'), re.IGNORECASE)
        if match:
            token = match.group(1)
            try:
                user = Token.objects.get(key=token).user
                return func(user=user, *args, **kwargs)
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    return wrapper


def json_check(func):
    def wrapper(*args, **kwargs):
        try:
            json_data = json.loads(args[0].body)
            return func(json_data=json_data, *args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    return wrapper
