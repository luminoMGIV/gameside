from shared.decorators import method_check

from .models import Category
from .serializers import CategorySerializer


@method_check
def category_list(request, method):
    data = CategorySerializer(Category.objects.all(), request=request)
    return data.json_response()


# @method_check
# def category_detail(request, category, method):
# try:
#     data = CategorySerializer(Category.objects.get(slug=slug), request=request)
#     return data.json_response()
# except Category.DoesNotExist:
#     return JsonResponse({'error': 'Category not found'}, status=404)


@method_check
def category_detail(request, category, method):
    return CategorySerializer(category, request=request).json_response()
