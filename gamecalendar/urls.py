from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_games, name='view-games'),
    path('add/', views.add_game, name='add-game-page'),
    path('add/<int:igdb_id>/', views.add_game, name='add-game'),
    path('search_igdb/', views.search_games, name='search-igdb'),
]
