from django.core import serializers
from django.shortcuts import render

from .models import Game, Review

# Create your views here.


def games_list(request):
    games = serializers.serialize('json', Game.objects.all())
    return render(request)


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
