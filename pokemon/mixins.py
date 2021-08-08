import requests

from django.views.generic.base import TemplateView


class PaginateTemplateMixin(TemplateView):
	""" Mixin for the main View that handles pagination
	of data retrieved from third-party API
	"""

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page: int = int(self.request.GET.get('page', 1))
		# Calculate offset (required for the third-party API request).
		offset = (page * 10 - 10)
		# Get proper page of pokemons from the API.
		pokemon_list = requests.get(
			f'https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit=10'
		).json()
		# If response contains no results - we're out of pokemons range.
		# Redirect to first page.
		if len(pokemon_list['results']) == 0:
			page = 1
			pokemon_list = requests.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=10').json()
		# Check if next page exists.
		if pokemon_list['next'] is None:
			context['next_page'] = None
		else:
			context['next_page'] = page + 1
		# Check if previous page exists.
		if pokemon_list['previous'] is None:
			context['previous_page'] = None
		else:
			context['previous_page'] = page - 1
		context['current_page'] = page
		# Save response data to the context.
		context['response'] = pokemon_list
		return context

