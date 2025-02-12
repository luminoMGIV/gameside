from django.http import Http404
from django.urls.converters import StringConverter

from .models import Platform


class PlatformConverter(StringConverter):
    def to_python(self, value):
        try:
            platform = Platform.objects.get(slug=value)
            return platform
        except Platform.DoesNotExist:
            raise Http404('Platform')

    def to_url(self, platform):
        return platform.slug
