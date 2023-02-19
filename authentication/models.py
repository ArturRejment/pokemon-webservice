from django.contrib.auth.models import AbstractUser
from django.db import models

from pokemon.models import Pokemon


class User(AbstractUser):
    favorite_pokemons = models.ManyToManyField(
        Pokemon, related_name="fav_pokemon", blank=True
    )

    def __str__(self):
        return self.username

    def favorite(self, pokemon: Pokemon) -> None:
        """Add specific pokemon to favorites"""
        self.favorite_pokemons.add(pokemon)

    def unfavorite(self, pokemon: Pokemon) -> None:
        """Remove specific pokemon from favorites"""
        self.favorite_pokemons.remove(pokemon)

    def is_favorite(self, pokemon_id: int) -> bool:
        """Returns True if pokemon is user's favorite. False otherwise"""
        try:
            Pokemon.objects.get(pokemon_id=pokemon_id)
        except Pokemon.DoesNotExist:
            return False
        return self.favorite_pokemons.filter(pokemon_id=pokemon_id).exists()
