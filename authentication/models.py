from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	favorite_pokemons = models.ManyToManyField('Pokemon', related_name='fav_pokemon', blank=True)

	def __str__(self):
		return self.username

	def favorite(self, pokemon):
		""" Add specific pokemon to favorites """
		self.favorite_pokemons.add(pokemon)

	def unfavorite(self, pokemon):
		""" Remove specific pokemon from favorites """
		self.favorite_pokemons.remove(pokemon)


class Pokemon(models.Model):
	pokemon_id = models.PositiveIntegerField(primary_key=True, unique=True, null=False, blank=False)
