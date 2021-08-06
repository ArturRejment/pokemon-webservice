import requests

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import sendPokemonRequest
from authentication.models import User, Pokemon


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


class FavoritePokemonsView(LoginRequiredMixin, TemplateView):
	template_name = 'pokemon/favorite.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		queryset = user.favorite_pokemons.all()

		pokemons_data = []
		for element in queryset:
			pokemon = sendPokemonRequest(element.pokemon_id)
			pokemons_data.append(pokemon)
		context['pokemon_data'] = pokemons_data
		return context


class AddPokemonToFavorite(LoginRequiredMixin, View):

	def post(self, request, **kwargs):
		user = request.user
		pokemon = Pokemon.objects.get_or_create(pokemon_id = kwargs['id'])
		user.favorite(pokemon[0])
		return redirect(reverse('main_page'))


class RemovePokemonFromFavorite(LoginRequiredMixin, View):

	def post(self, request, **kwargs):
		user = request.user
		try:
			pokemon = Pokemon.objects.get(pokemon_id = kwargs['id'])
		except Pokemon.DoesNotExist:
			raise ValueError('Pokemon with this id does not exist')
		user.unfavorite(pokemon)
		return redirect(reverse('favorite_pokemons'))

