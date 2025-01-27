from django.core import serializers
from django.shortcuts import render

from .models import Game, Review

# Create your views here.


def game_list(request):
    if request.method == 'GET':
        games = serializers.serialize('json', Game.objects.all())
        games_data = [{'name': game.name, 'description': game.description} for game in games]
        return JsonResponse({'games': games_data}, status=200)
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)



def games_detail(request, title):
    game = serializers.serialize('json', Game.objects.get(title=title))

    return render(request)


def review_list(request):
    reviews = serializers.serialize('json', Review.objects.all())
    return render(request)


def review_detail(request, pk):
    review = serializers.serialize('json', Review.objects.get(pk=pk))
    return render(request)


def add_review(request):
    pass
