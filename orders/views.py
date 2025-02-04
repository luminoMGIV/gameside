from shared.decorators import method_check

from .models import Order
from .serializers import OrderSerializer


@method_check('POST')
def add_order(request):
    pass


@method_check('GET')
def order_detail(request, pk):
    data = OrderSerializer(Order.objects.get(pk=pk))
    return data.json_response()


@method_check('POST')
def confirm_order(request):
    pass


@method_check('POST')
def cancel_order(request):
    pass


@method_check('POST')
def pay_order(request):
    pass
