from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import json_check, method_check, user_check

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@method_check
def game_list(request, method):
    games = Game.objects.all()
    for key, value in request.GET.items():
        filter_key = f'{key}s__name' if key == 'platform' else f'{key}__name'
        games = games.filter(**{filter_key: value})
    data = GameSerializer(games, request=request)
    return data.json_response()


# @method_check
# def games_detail(request, slug, method):
#     try:
#         game = Game.objects.get(slug=slug)
#         data = GameSerializer(game, request=request)
#         return data.json_response()
#     except Game.DoesNotExist:
#         return JsonResponse({'error': 'Game not found'}, status=404)


# @method_check
# def review_list(request, slug, method):
#     try:
#         game = Game.objects.get(slug=slug)
#         data = ReviewSerializer(game.reviews.all(), request=request)
#         return data.json_response()
#     except Game.DoesNotExist:
#         return JsonResponse({'error': 'Game not found'}, status=404)


# @csrf_exempt
# @method_check
# def review_detail(request, pk, method):
#     try:
#         review = Review.objects.get(pk=pk)
#         data = ReviewSerializer(review, request=request)
#         return data.json_response()
#     except Review.DoesNotExist:
#         return JsonResponse({'error': 'Review not found'}, status=404)


# @csrf_exempt
# @method_check
# @json_check
# @user_check
# def add_review(request, slug, user, json_data, method,):
#     try:
#         game = Game.objects.get(slug=slug)
#         try:
#             review = Review.objects.create(
#                 rating=json_data['rating'],
#                 comment=json_data['comment'],
#                 game=game,
#                 author=user,
#             )
#             review.full_clean()
#             review.save()
#             return JsonResponse({'id': review.pk}, status=200)
#         except ValidationError:
#             return JsonResponse({'error': 'Rating is out of range'}, status=400)
#     except Game.DoesNotExist:
#         return JsonResponse({'error': 'Game not found'}, status=404)


@method_check
def games_detail(request, game, method):
    return GameSerializer(game, request=request).json_response()


@method_check
def review_list(request, game, method):
    return ReviewSerializer(game.reviews.all(), request=request).json_response()


@csrf_exempt
@method_check
def review_detail(request, review, method):
    return ReviewSerializer(review, request=request).json_response()


@csrf_exempt
@method_check
@json_check
@user_check
def add_review(request, game, user, json_data, method, fields):
    try:
        review = Review.objects.create(
            rating=json_data['rating'],
            comment=json_data['comment'],
            game=game,
            author=user,
        )
        review.full_clean()
        review.save()
        return JsonResponse({'id': review.pk}, status=200)
    except ValidationError:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
