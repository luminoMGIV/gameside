from django.http import Http404
from django.urls.converters import IntConverter

from .models import Order


class OrderConverter(IntConverter):
    def to_python(self, value):
        try:
            order = Order.objects.get(pk=int(value))
            return order
        except Order.DoesNotExist:
            raise Http404('Order')

    def to_url(self, order):
        return order.pk
