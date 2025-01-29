import json

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import method_check

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@method_check(method='GET')
def game_list(request):
    data = GameSerializer(Game.objects.all())
    return data.json_response()


@method_check(method='GET')
def games_detail(request, slug):
    data = GameSerializer(Game.objects.get(slug=slug))
    return data.json_response()


@method_check(method='GET')
def review_list(request):
    data = ReviewSerializer(Review.objects.all())
    return data.json_response()


@csrf_exempt
# @method_check(method='GET')
def review_detail(request, pk):
    data = ReviewSerializer(Review.objects.get(pk=pk))
    return data.json_response()


@csrf_exempt
@method_check('POST')
def add_review(request, slug):
    data = json.loads(request.body)
    review = Review.objects.create(
        rating=data['rating'],
        comment=data['comment'],
        game=Game.objects.get(pk=int(data['game'])),
        author=User.objects.get(pk=int(data['author'])),
    )
    return redirect('games:review-detail', pk=review.pk)
