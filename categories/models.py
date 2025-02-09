from colorfield.fields import ColorField
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(name)
    description = models.TextField(blank=True)
    color = ColorField(default='#ffffff')
