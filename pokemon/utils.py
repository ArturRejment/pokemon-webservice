import requests

def sendPokemonRequest(num):
	dictionary = {}
	# Fetch single pokemon
	response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{num}').json()
	# Get only necessary fields
	dictionary['name'] = response['name']
	dictionary['id'] = response['id']
	types = []
	# Create a list of pokemon's types
	for type in response['types']:
		types.append(type['type']['name'])
	dictionary['types'] = types
	return dictionary

def getEvolutionChain(response):
	# Handle evelution chain creation
	pokemon_species_url = response['species']['url']
	pokemon_species = requests.get(pokemon_species_url).json()
	pokemon_evolution_chain_url = pokemon_species['evolution_chain']['url']
	pokemon_evolution_chain = requests.get(pokemon_evolution_chain_url).json()
	evolution_chain_data = []
	evolves_to = pokemon_evolution_chain['chain']
	evolution_chain_data.append( requests.get(f'https://pokeapi.co/api/v2/pokemon/{evolves_to["species"]["name"]}/').json())
	evolves_to = evolves_to['evolves_to']
	while len(evolves_to) != 0:
		name = evolves_to[0]['species']['name']
		pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}/').json()
		evolution_chain_data.append(pokemon)
		evolves_to = evolves_to[0]['evolves_to']
	return evolution_chain_data