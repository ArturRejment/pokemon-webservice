import requests

from django.views.generic.base import TemplateView


class PaginateTemplateMixin(TemplateView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page: int = int(self.request.GET.get('page', 1))
		offset = (page*10 - 10)
		response = requests.get(f'https://pokeapi.co/api/v2/pokemon/?offset={offset}&limit=10').json()
		if len(response['results']) == 0:
			page = 1
			response = requests.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=10').json()
		# Check if next page exists
		if response['next'] is None:
			context['next_page'] = None
		else:
			context['next_page'] = page + 1
		# Check if previous page exists
		if response['previous'] is None:
			context['previous_page'] = None
		else:
			context['previous_page'] = page - 1
		context['current_page'] = page
		# Save response data to the context
		context['response'] = response
		return context

