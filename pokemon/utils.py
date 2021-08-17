import requests
from operator import itemgetter

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings

from .worker import ThreadPool
from authentication.models import Pokemon

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def extractIdFromUrl(url: str) -> int:
	splitted_url = url.split('/')
	return int(splitted_url[-2])


def getPokemonsCachedData(user, pokemon_id_list: int) -> list:
	"""Retrieve cached information about Pokemon with Redis or
	send request and cache it if is not present

	Args:
		user (User): User instance fetched from request
		pokemon_id (int): Id of pokemon whose data is going to be
						  fetched
	"""
	pokemons_data = []
	for pokemon_id in pokemon_id_list:
		# Try to retrieve pokemon form cache
		if cache.get(pokemon_id):
			pokemon = cache.get(pokemon_id)
		else:
		# If pokemon does not exist in cache
		# Send request to obtain data and save it to the cache
			pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()
			cache.set(pokemon_id, pokemon)
		# Check if this particular pokemon is user's favorite
		try:
			pokemon_object = Pokemon.objects.get(pokemon_id=pokemon['id'])
		except Pokemon.DoesNotExist:
			pokemon['is_favorite_pokemon'] = False
		else:
			pokemon['is_favorite_pokemon'] = user.is_favorite(pokemon_object)
		pokemons_data.append(pokemon)
	return pokemons_data


def getEvolutionChain(user, response) -> list:
	""" A Function to fetch data about all pokemons in particular
		evolution chain

	Args:
		user ([User]): [User instance fetched from request]
		response ([type]): [description]

	Returns:
		list: [List of dictionaries with pokemon details]
	"""
	# Get pokemon species url - necessary to fetch evolution chain.
	pokemon_species_url = response['species']['url']
	pokemon_species = requests.get(pokemon_species_url).json()
	# Get url for the evolution chain.
	pokemon_evolution_chain_url = pokemon_species['evolution_chain']['url']
	# Fetch data about evolution chain.
	pokemon_evolution_chain = requests.get(pokemon_evolution_chain_url).json()
	# Create a list to store urls of every pokemon present in the chain.
	evolution_chain_ids = []
	# Create url for first pokemon in the chain.
	evolves_to = pokemon_evolution_chain['chain']
	evolution_chain_ids.append(
		extractIdFromUrl(evolves_to["species"]["url"])
	)
	# Fetch other pokemons present in the chain as long as they exist.
	evolves_to = evolves_to['evolves_to']
	while len(evolves_to) != 0:
		id = extractIdFromUrl(evolves_to[0]['species']['url'])
		# Fetch data about specific pokemon in the chain.
		evolution_chain_ids.append(id)
		evolves_to = evolves_to[0]['evolves_to']
	# Return list with data about all pokemons in evelution chain.
	return getPokemonsCachedData(user, evolution_chain_ids)