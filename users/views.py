import json
from django.contrib.auth import authenticate

from shared.decorators import method_check, json_check
from django.http import JsonResponse

@method_check('POST')
@json_check(['username', 'password'])
def auth(request, json_data):
    username = json_data['username']
    password = json_data['password']
    if (user:= authenticate(username=username, password=password)):
        return JsonResponse({'token': user.token.key }, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
