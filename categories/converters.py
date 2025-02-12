from django.http import Http404
from django.urls.converters import StringConverter

from .models import Category


class CategoryConverter(StringConverter):
    def to_python(self, value):
        try:
            category = Category.objects.get(slug=value)
            return category
        except Category.DoesNotExist:
            raise Http404('Category')

    def to_url(self, category):
        return category.slug
