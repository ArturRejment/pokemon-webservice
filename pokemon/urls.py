from django.urls import path

from .views import (AddPokemonToFavorite, DetailPageView, FavoritePokemonsView,
                    MainPageView, RemovePokemonFromFavorite)

urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path("favorite/", FavoritePokemonsView.as_view(), name="favorite_pokemons"),
    path(
        "favorite_pokemon/<int:id>/",
        AddPokemonToFavorite.as_view(),
        name="favorite_pokemon",
    ),
    path(
        "unfavorite_pokemon/<int:id>/",
        RemovePokemonFromFavorite.as_view(),
        name="unfavorite_pokemon",
    ),
    path("pokemon/<int:id>/", DetailPageView.as_view(), name="pokemon_detail"),
]
