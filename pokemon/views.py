import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView

from authentication.models import Pokemon, User

from .mixins import PaginateTemplateMixin
from .utils import extract_id_from_url, get_evolution_chain, get_pokemons_cached_data


class MainPageView(LoginRequiredMixin, PaginateTemplateMixin):
    template_name: str = "pokemon/index.html"

    def get_context_data(self, **kwargs):
        # Get the context
        context = super().get_context_data(**kwargs)
        response = context["response"]
        pokemon_id_list = [
            extract_id_from_url(element["url"]) for element in response["results"]
        ]
        context["pokemon_data"] = get_pokemons_cached_data(
            self.request.user, pokemon_id_list
        )
        return context


class DetailPageView(LoginRequiredMixin, TemplateView):
    template_name: str = "pokemon/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon_id = []
        pokemon_id.append(kwargs["id"])
        pokemon_data = get_pokemons_cached_data(self.request.user, pokemon_id)
        context["pokemon_data"] = pokemon_data[0]
        context["evolution_chain"] = get_evolution_chain(
            self.request.user, pokemon_data[0]
        )
        return context


class FavoritePokemonsView(LoginRequiredMixin, TemplateView):
    template_name: str = "pokemon/favorite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = user.favorite_pokemons.all()
        # Create list with urls for user's favorite pokemons
        id_list = [element.pokemon_id for element in queryset]
        # Add pokemons data to the context
        context["pokemon_data"] = get_pokemons_cached_data(self.request.user, id_list)
        return context


class AddPokemonToFavorite(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user = request.user
        pokemon, _ = Pokemon.objects.get_or_create(pokemon_id=kwargs["id"])
        user.favorite(pokemon)
        return redirect(request.META.get("HTTP_REFERER"))


class RemovePokemonFromFavorite(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user = request.user
        try:
            pokemon = Pokemon.objects.get(pokemon_id=kwargs["id"])
        except Pokemon.DoesNotExist:
            raise ValueError("Pokemon with this id does not exist")
        user.unfavorite(pokemon)
        return redirect(request.META.get("HTTP_REFERER"))
