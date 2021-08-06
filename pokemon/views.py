import requests

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import sendPokemonRequest


class MainPageView(LoginRequiredMixin, TemplateView):
	template_name = 'pokemon/index.html'

	def get_context_data(self, **kwargs):
		# Get the context
		context = super().get_context_data(**kwargs)
		# Set PokeAPI pagination
		page = self.request.GET.get('page', 1)
		offset = (int(page) * 10 - 9)
		payload = {'limit':10, 'offset': offset}

		# Make a list of fetched pokemons
		pokemons_data = []
		for num in range(offset, offset+10):
			pokemon = sendPokemonRequest(num)
			# Append data to the pokemons list
			pokemons_data.append(pokemon)
		# Add pokemons data to the context
		context['pokemon_data'] = pokemons_data
		return context


class DetailPageView(LoginRequiredMixin, TemplateView):
	template_name = 'pokemon/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pokemon_id = kwargs['id']
		response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()
		context['pokemon_data'] = response
		return context
