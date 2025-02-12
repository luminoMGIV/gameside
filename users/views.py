from django.contrib.auth import authenticate
from django.http import JsonResponse
from shared.decorators import json_check, method_check


@method_check
@json_check
def auth(request, json_data, method, fields):
    username = json_data['username']
    password = json_data['password']
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
