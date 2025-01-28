from shared.decorators import method_check

from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@method_check('GET')
def category_list(request):
    data = CategorySerializer(Category.objects.all())
    return data.json_response()


@method_check('GET')
def category_detail(request, slug):
    data = CategorySerializer(Category.objects.get(slug=slug))
    return data.json_response()
