from django.http import JsonResponse
from shared.decorators import method_check

from .models import Category
from .serializers import CategorySerializer


@method_check('GET')
def category_list(request):
    data = CategorySerializer(Category.objects.all())
    return data.json_response()


@method_check('GET')
def category_detail(request, slug):
    try:
        data = CategorySerializer(Category.objects.get(slug=slug))
        return data.json_response()
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
