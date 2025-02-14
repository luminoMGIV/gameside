from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def update_stock(instance, created, *args, **kwargs):
    if not created:
        if game:= instance.game:
            game.stock -= 1
            game.save()
        elif instance.status == Order.Status.CANCELLED:
            for game in instance.games.all():
                game.stock += 1
                game.save()
        delattr(instance, 'game')
