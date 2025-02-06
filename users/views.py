import json
from django.contrib.auth import get_user_model

from shared.decorators import method_check, json_check
from django.http import JsonResponse

@method_check('POST')
@json_check
def auth(request, json_data):
    User = get_user_model()
    if (username:= json_data.get('username', None)) and (password:= json_data.get('password', None)):
        if (user:= User.objects.get(username=username)).password == password:
            return JsonResponse({'token': user.token}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Missing required fields'}, status=400)
