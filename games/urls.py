from django.urls import path, register_converter

from . import views
from .converters import GameConverter, ReviewConverter

app_name = 'games'

register_converter(GameConverter, 'game')
register_converter(ReviewConverter, 'review')

# urlpatterns = [
#     path('', views.game_list, {'method': 'GET'}, name='game-list'),
#     path('<str:slug>/', views.games_detail, {'method': 'GET'}, name='games-detail'),
#     path('<str:slug>/reviews/', views.review_list, {'method': 'GET'}, name='review-list'),
#     path(
#         '<str:slug>/reviews/add/',
#         views.add_review,
#         {'method': 'POST', 'fields': ['rating', 'comment']},
#         name='add-review',
#     ),
#     path('reviews/<int:pk>/', views.review_detail, {'method': 'GET'}, name='review-detail'),
# ]


urlpatterns = [
    path('', views.game_list, {'method': 'GET'}, name='game-list'),
    path('<game:game>/', views.games_detail, {'method': 'GET'}, name='games-detail'),
    path('<game:game>/reviews/', views.review_list, {'method': 'GET'}, name='review-list'),
    path(
        '<game:game>/reviews/add/',
        views.add_review,
        {'method': 'POST', 'fields': ['rating', 'comment']},
        name='add-review',
    ),
    path('reviews/<review:review>/', views.review_detail, {'method': 'GET'}, name='review-detail'),
]
