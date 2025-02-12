from django.http import Http404
from django.urls.converters import IntConverter, StringConverter

from .models import Game, Review


class GameConverter(StringConverter):
    def to_python(self, value):
        try:
            game = Game.objects.get(slug=value)
            return game
        except Game.DoesNotExist:
            raise Http404('Game')

    def to_url(self, game):
        return game.slug


class ReviewConverter(IntConverter):
    def to_python(self, value):
        try:
            review = Review.objects.get(pk=int(value))
            return review
        except Review.DoesNotExist:
            raise Http404('Review')

    def to_url(self, review):
        return review.slug
