from django.urls import path

from . import views

app_name = 'games'


urlpatterns = [
    path('', views.game_list, {'method': 'GET'}, name='game-list'),
    path('<str:slug>/', views.games_detail, {'method': 'GET'}, name='games-detail'),
    path('<str:slug>/reviews/', views.review_list, {'method': 'GET'}, name='review-list'),
    path(
        '<str:slug>/reviews/add/',
        views.add_review,
        {'method': 'POST', 'fields': ['rating', 'comment']},
        name='add-review',
    ),
    path('reviews/<int:pk>/', views.review_detail, {'method': 'GET'}, name='review-detail'),
]
