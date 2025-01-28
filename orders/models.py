import uuid

from django.conf import settings
from django.db import models

# Create your models here.


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3

    status = models.IntegerField(choices=Status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    games = models.ManyToManyField('games.Game', related_name='orders')

    def __str__(self):
        return str(self.pk)
