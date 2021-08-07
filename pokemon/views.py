import requests

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import getPokemonsData, getEvolutionChain
from .mixins import PaginateTemplateMixin
from authentication.models import User, Pokemon


class MainPageView(LoginRequiredMixin, PaginateTemplateMixin):
	template_name: str = 'pokemon/index.html'

	def get_context_data(self, **kwargs):
		# Get the context
		context = super().get_context_data(**kwargs)
		response = context['response']
		url_list = [f'https://pokeapi.co/api/v2/pokemon/{element["name"]}' for element in response['results']]
		context['pokemon_data'] = getPokemonsData(url_list, len(response['results']))
		return context


class DetailPageView(LoginRequiredMixin, TemplateView):
	template_name: str = 'pokemon/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pokemon_id = kwargs['id']
		response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/').json()
		context['pokemon_data'] = response
		context['evolution_chain'] = getEvolutionChain(response)
		return context


class FavoritePokemonsView(LoginRequiredMixin, TemplateView):
	template_name: str = 'pokemon/favorite.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		queryset = user.favorite_pokemons.all()

		url_list = [f'https://pokeapi.co/api/v2/pokemon/{element.pokemon_id}' for element in queryset]

		context['pokemon_data'] = getPokemonsData(url_list, len(queryset))
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

