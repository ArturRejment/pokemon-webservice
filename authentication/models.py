from django.db import models
from django.contrib.auth.models import AbstractUser

from pokemon.models import Pokemon


class User(AbstractUser):
	favorite_pokemons = models.ManyToManyField(Pokemon, related_name='fav_pokemon', blank=True)

	def __str__(self):
		return self.username

	def favorite(self, pokemon):
		""" Add specific pokemon to favorites """
		self.favorite_pokemons.add(pokemon)

	def unfavorite(self, pokemon):
		""" Remove specific pokemon from favorites """
		self.favorite_pokemons.remove(pokemon)

	def is_favorite(self, pokemon):
		""" Returns True if pokemon is user's favorite. False otherwise """
		return self.favorite_pokemons.filter(pokemon_id = pokemon.pokemon_id).exists()
