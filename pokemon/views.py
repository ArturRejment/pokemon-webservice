import requests

from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
	template_name = 'pokemon/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pokemon_data'] = requests.get('https://pokeapi.co/api/v2/pokemon/').json()['results']
		return context
