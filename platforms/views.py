from shared.decorators import method_check

from .models import Platform
from .serializers import PlatformSerializer


@method_check
def platform_list(request, method):
    data = PlatformSerializer(Platform.objects.all(), request=request)
    return data.json_response()


# @method_check
# def platform_detail(request, slug, method):
#     try:
#         data = PlatformSerializer(Platform.objects.get(slug=slug), request=request)
#         return data.json_response()
#     except Platform.DoesNotExist:
#         return JsonResponse({'error': 'Platform not found'}, status=404)


@method_check
def platform_detail(request, platform, method):
    return PlatformSerializer(platform, request=request).json_response()
