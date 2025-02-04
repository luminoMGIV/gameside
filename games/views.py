import json
import re

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import method_check
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
    data = ReviewSerializer(Review.objects.all())
    return data.json_response()


@csrf_exempt
@method_check(method='GET')
def review_detail(request, pk):
    try:
        data = ReviewSerializer(Review.objects.get(pk=pk))
        return data.json_response()
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)


@csrf_exempt
@method_check('POST')
def add_review(request, slug):
    regular_expression = r'?P<token> ^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$ '

    pattern = re.fullmatch(request.headers, regular_expression)
    token = pattern['token']
    data = json.loads(request.body)
    game = Game.objects.get(slug=slug)
    user = Token.objects.get(key=data['token']).user
    review = Review.objects.create(
        rating=data['rating'],
        comment=data['comment'],
        game=game,
        author=user,
    )

    return redirect('games:review-detail', pk=review.pk)
