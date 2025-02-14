import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1

    status = models.IntegerField(choices=Status, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    games = models.ManyToManyField('games.Game', related_name='orders')

    def __str__(self):
        return str(self.pk)
    
    @property
    def price(self):
        return sum(game.price for game in self.games.all())
    
    def save(self, game=None, *args, **kwargs):
        self.game = game
        super(Order, self).save(*args, **kwargs)
    
    def change_status(self, status):
        self.status = status
        self.save()

    def add_game(self, game):
        self.games.add(game)
        self.save(game)