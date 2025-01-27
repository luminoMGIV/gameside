from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('filter/', views.game_list, name='filter'),
    path('<str:title>/', views.games_detail, name='games-detail'),
    path('<str:title>/reviews/', views.review_list, name='review-list'),
    path('<str:title>/reviews/add/', views.add_review, name='add-review'),
    path('reviews/<int:pk>', views.review_detail, name='review-detail'),
]
