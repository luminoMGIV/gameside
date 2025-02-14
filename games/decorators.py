from django.http import JsonResponse
from .models import Game

def game_check(func):
    def wrapper(*args, **kwargs):
        try:
            slug = kwargs.get('slug')
            game = Game.objects.get(slug=slug)
            return func(game=game, *args, **kwargs)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

    return wrapper
