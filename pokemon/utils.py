import requests
from operator import itemgetter

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings

from .worker import ThreadPool
from authentication.models import Pokemon

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def getPokemonData(user, pokemon_id: int):
	"""Retrieve cached information about Pokemon with Redis or
	send request and cache it if is not present

	Args:
		user (User): User instance fetched from request
		pokemon_id (int): Id of pokemon whose data is going to be
						  fetched
	"""
	if cache.get(pokemon_id):
		pokemon = cache.get(pokemon_id)
		print('POKEMON FROM CACHE')
	else:
		pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()
		cache.set(pokemon_id, pokemon)
		print('POKEMON FROM REQUEST')
	return pokemon


def getPokemonsData(user, url_list: list, pool_size: int) -> list:
	"""A function to send requests using threads in order to
		retrieve details about pokomons

	Args:
		user ([User]): [User instance fetched from request]
		url_list (list): [List of urls for every pokemon]
		pool_size (int): [Number of pokemons - to add proper number of
						  tasks]

	Returns:
		list: [List of dictionaries with pokemon details]
	"""

	pool = ThreadPool(pool_size)
	r = requests.session()
	# Create blank list to store json's with details about pokemons.
	results = []
	# Declare new fuction to send requests and store the results.
	def get(url):
		resp = r.get(url).json()
		results.append(resp)
	# Add a list of tasks to the queue.
	pool.map(get, url_list)
	# Wait untill all of the tasks are completed.
	pool.wait_completion()
	# Sort the resutls growingly by pokemon id.
	results = sorted(results, key=itemgetter('id'))
	# Check if pokemon is user's favorite.
	for item in results:
		try:
			pokemon = Pokemon.objects.get(pokemon_id=item['id'])
		except Pokemon.DoesNotExist:
			item['is_favorite_pokemon'] = False
		else:
			item['is_favorite_pokemon'] = user.is_favorite(pokemon)

	return results


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
	evolution_chain_urls = []
	# Create url for first pokemon in the chain.
	evolves_to = pokemon_evolution_chain['chain']
	evolution_chain_urls.append(
		f'https://pokeapi.co/api/v2/pokemon/{evolves_to["species"]["name"]}/'
	)
	# Fetch other pokemons present in the chain as long as they exist.
	evolves_to = evolves_to['evolves_to']
	while len(evolves_to) != 0:
		name = evolves_to[0]['species']['name']
		# Fetch data about specific pokemon in the chain.
		evolution_chain_urls.append(f'https://pokeapi.co/api/v2/pokemon/{name}/')
		evolves_to = evolves_to[0]['evolves_to']
	# Return list with data about all pokemons in evelution chain.
	return getPokemonsData(user, evolution_chain_urls, len(evolution_chain_urls))