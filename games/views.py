import json
import re

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import method_check, user_check, json_check
from users.models import Token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@method_check(method='GET')
def game_list(request):
    data = GameSerializer(Game.objects.all(), request=request)
    return data.json_response()


@method_check(method='GET')
def games_detail(request, slug):
    try:
        data = GameSerializer(Game.objects.get(slug=slug), request=request)
        return data.json_response()
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)


@method_check(method='GET')
def review_list(request, slug):
    data = ReviewSerializer(Review.objects.all(), request=request)
    return data.json_response()


@csrf_exempt
@method_check(method='GET')
def review_detail(request, pk):
    try:
        data = ReviewSerializer(Review.objects.get(pk=pk), request=request)
        return data.json_response()
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)


@csrf_exempt
@method_check('POST')
@user_check
@json_check
def add_review(request, slug, user, json_data):
    try:
        game = Game.objects.get(slug=slug)
        if (rating:= json_data['rating']) and (comment:= json_data['comment']):
            if 1 <= rating <= 5:
                review = Review.objects.create(
                    rating=rating,
                    comment=comment,
                    game=game,
                    author=user,
                )
                return JsonResponse({'id': review.pk }, status=200)
            return JsonResponse({'error': 'Rating is out of range' }, status=400)
        return JsonResponse({'error': 'Missing required fields' }, status=400)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found' }, status=404)