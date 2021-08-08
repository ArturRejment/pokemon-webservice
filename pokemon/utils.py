import requests
from operator import itemgetter

from .worker import ThreadPool
from authentication.models import Pokemon


def getPokemonsData(user, url_list: list, pool_size: int) -> list:
	""" A function to send requests using threads in order to retrieve details about pokomons """

	# New ThreadPool
	pool = ThreadPool(pool_size)
	# Open a session
	r = requests.session()
	# Create blank list to store json's with details about pokemons
	results = []
	# Declare new fuction to send requests and store the results
	def get(url):
		resp = r.get(url).json()
		# Check if pokemon is user's favorite
		results.append(resp)
	# Map every url with the 'get' function
	pool.map(get, url_list)
	# Wait untill all of the threads are completed
	pool.wait_completion()
	# Sort the resutls growingly by pokemon id
	results = sorted(results, key=itemgetter('id'))
	for item in results:
		try:
			pokemon = Pokemon.objects.get(pokemon_id=item['id'])
		except Pokemon.DoesNotExist:
			item['is_favorite_pokemon'] = False
		else:
			item['is_favorite_pokemon'] = user.is_favorite(pokemon)

	return results


def getEvolutionChain(user, response) -> list:
	""" Handle evelution chain creation """
	# Get pokemon species url - necessary to fetch proper evolution chain
	pokemon_species_url = response['species']['url']
	pokemon_species = requests.get(pokemon_species_url).json()
	# Get url to the evolution chain
	pokemon_evolution_chain_url = pokemon_species['evolution_chain']['url']
	# Fetch evolution chain
	pokemon_evolution_chain = requests.get(pokemon_evolution_chain_url).json()
	# Create blank list to store urls of every pokemon present in the chain
	evolution_chain_urls = []
	# Create url for first
	evolves_to = pokemon_evolution_chain['chain']
	evolution_chain_urls.append(
		f'https://pokeapi.co/api/v2/pokemon/{evolves_to["species"]["name"]}/'
	)
	# Fetch other pokemons in chain as long as they exist
	evolves_to = evolves_to['evolves_to']
	while len(evolves_to) != 0:
		name = evolves_to[0]['species']['name']
		# Fetch data about specific pokemon in the chain
		evolution_chain_urls.append(f'https://pokeapi.co/api/v2/pokemon/{name}/')
		evolves_to = evolves_to[0]['evolves_to']
	# Return list with entire data about all pokemons available in evelution chain
	return getPokemonsData(user, evolution_chain_urls, len(evolution_chain_urls))