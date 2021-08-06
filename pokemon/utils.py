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