from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.PositiveIntegerField(
        primary_key=True, unique=True, null=False, blank=False
    )
