from django.db import models

# Create your models here.


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True, default='/logos/default.jpg')

    def __str__(self):
        return self.name
