from colorfield.fields import ColorField
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(name)
    description = models.TextField(blank=True)
    color = ColorField(default='#FF0000')
