import requests

from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
	template_name = 'pokemon/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page = self.request.GET.get('page', 1)
		offset = (int(page) * 10 - 10)
		payload = {'limit':10, 'offset': offset}
		pokemons_data = requests.get('https://pokeapi.co/api/v2/pokemon/', params=payload).json()['results']
		data = []
		for pokemon in pokemons_data:
			dictionary = {}
			response = requests.get(pokemon['url']).json()
			dictionary['name'] = response['name']
			dictionary['id'] = response['id']
			types = []
			for type in response['types']:
				types.append(type['type']['name'])
			dictionary['types'] = types
			data.append(dictionary)
			# print(data)
		print(data)
		context['pokemon_data'] = data
		return context
