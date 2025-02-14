from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import json_check, method_check, user_check

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer
from .decorators import game_check


@method_check
def game_list(request, method):
    games = Game.objects.all()
    for key, value in request.GET.items():
        filter_key = f'{key}s__slug' if key == 'platform' else f'{key}__slug'
        games = games.filter(**{filter_key: value})
    data = GameSerializer(games, request=request)
    return data.json_response()


@method_check
@game_check
def games_detail(request, slug, method, game):
    data = GameSerializer(game, request=request)
    return data.json_response()


@method_check
@game_check
def review_list(request, slug, method, game):
    data = ReviewSerializer(game.reviews.all(), request=request)
    return data.json_response()


@method_check
def review_detail(request, pk, method):
    try:
        review = Review.objects.get(pk=pk)
        data = ReviewSerializer(review, request=request)
        return data.json_response()
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)


@csrf_exempt
@method_check
@json_check
@user_check
@game_check
def add_review(request, slug, user, json_data, method, fields, game):
    try:
        review = Review.objects.create(
            rating=json_data['rating'],
            comment=json_data['comment'],
            game=game,
            author=user,
        )
        review.full_clean()
        review.save()
        return JsonResponse({'id': review.pk})
    except ValidationError:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
