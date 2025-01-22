from django.core import serializers
from django.http import JsonResponse

from .models import Platform

# Create your views here.


def platform_list(request):
    platforms = serializers.serialize('json', Platform.objects.all())
    return JsonResponse(platforms, safe=False)


def platform_detail(request):
    pass
