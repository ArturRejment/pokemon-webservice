import requests


def sendPokemonRequest(num: int) -> dict:
	dictionary: dict = {}
	# Fetch single pokemon
	response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}').json()
	# Get only necessary fields
	dictionary['name'] = response['name']
	dictionary['id'] = response['id']
	types: list = []
	# Create a list of pokemon's types
	for type in response['types']:
		types.append(type['type']['name'])
	dictionary['types'] = types
	return dictionary


def getEvolutionChain(response) -> list:
	""" Handle evelution chain creation """
	# Get pokemon species url - necessary to fetch proper evolution chain
	pokemon_species_url = response['species']['url']
	pokemon_species = requests.get(pokemon_species_url).json()
	# Get url to the evolution chain
	pokemon_evolution_chain_url = pokemon_species['evolution_chain']['url']
	# Fetch evolution chain
	pokemon_evolution_chain = requests.get(pokemon_evolution_chain_url).json()
	# Create blank list to store data of every pokemon present in the chain
	evolution_chain_data = []
	# Fetch first pokemon in the chain
	evolves_to = pokemon_evolution_chain['chain']
	evolution_chain_data.append(
		requests.get(f'https://pokeapi.co/api/v2/pokemon/{evolves_to["species"]["name"]}/').json()
	)
	# Fetch other pokemons in chain as long as they exist
	evolves_to = evolves_to['evolves_to']
	while len(evolves_to) != 0:
		name = evolves_to[0]['species']['name']
		# Fetch data about specific pokemon in the chain
		pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/').json()
		# Add this pokemon to the list
		evolution_chain_data.append(pokemon)
		evolves_to = evolves_to[0]['evolves_to']
	# Return list with entire data about all pokemons available in evelution chain
	return evolution_chain_data