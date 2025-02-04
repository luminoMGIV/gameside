from django.http import JsonResponse
from shared.decorators import method_check

from .models import Platform
from .serializers import PlatformSerializer


@method_check('GET')
def platform_list(request):
    data = PlatformSerializer(Platform.objects.all(), request=request)
    return data.json_response()


@method_check('GET')
def platform_detail(request, slug):
    try:
        data = PlatformSerializer(Platform.objects.get(slug=slug), request=request)
        return data.json_response()
    except Platform.DoesNotExist:
        return JsonResponse({'error': 'Platform not found'}, status=404)
