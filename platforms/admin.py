from django.contrib import admin

from .models import Platform

# Register your models here.


@admin.register(Platform)
class Platform(admin.ModelAdmin):
    list_display = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
