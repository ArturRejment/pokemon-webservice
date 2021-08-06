from django.urls import path
from .views import MainPageView, DetailPageView, FavoritePokemonsView, AddPokemonToFavorite

urlpatterns = [
	path('', MainPageView.as_view(), name='main_page'),
	path('favorite/', FavoritePokemonsView.as_view(), name='favorite_pokemons'),
	path('manage_favorites/<int:id>/', AddPokemonToFavorite.as_view(), name='manage_favorites'),
	path('pokemon/<int:id>/', DetailPageView.as_view(), name='pokemon_detail'),
]
