# from django.core import serializers
from django.shortcuts import render

from .models import Order

# Create your views here.


def add_order(request):
    pass


def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request)


def confirm_order(request):
    pass


def cancel_order(request):
    pass


def pay_order(request):
    pass
