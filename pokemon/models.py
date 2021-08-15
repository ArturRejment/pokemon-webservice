from django.db import models


class Pokemon(models.Model):
	""" Pokemon model to store """
	pokemon_id = models.PositiveIntegerField(
		primary_key=True, unique=True,
		null=False, blank=False
	)
