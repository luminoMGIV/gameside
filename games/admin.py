from django.contrib import admin

from .models import Game, Review

# Register your models here.


@admin.register(Game)
class Game(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'stock']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = ['comment', 'rating']
