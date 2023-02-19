import requests
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def extract_id_from_url(url: str) -> int:
    return int(url.split("/")[-2])


def get_pokemon_data(pokemon_id: int) -> dict:
    """
    Return pokemon data from cache, or fetch pokemon data from API and save it in cache.
    """
    if pokemon := cache.get(pokemon_id):
        return pokemon

    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}").json()
    cache.set(pokemon_id, pokemon)
    return pokemon


def get_pokemons_cached_data(user, pokemon_id_list: list[int]) -> list:
    pokemons_data = []
    for pokemon_id in pokemon_id_list:
        pokemon = get_pokemon_data(pokemon_id)
        pokemon["is_favorite_pokemon"] = user.is_favorite(pokemon_id)
        pokemons_data.append(pokemon)

    return pokemons_data


def get_evolution_chain(user, response) -> list:
    # Get pokemon species url - necessary to fetch evolution chain.
    pokemon_species_url = response["species"]["url"]
    pokemon_species = requests.get(pokemon_species_url).json()
    # Get url for the evolution chain.
    pokemon_evolution_chain_url = pokemon_species["evolution_chain"]["url"]
    # Fetch data about evolution chain.
    pokemon_evolution_chain = requests.get(pokemon_evolution_chain_url).json()
    # Create a list to store urls of every pokemon present in the chain.
    evolution_chain_ids = []
    # Create url for first pokemon in the chain.
    evolves_to = pokemon_evolution_chain["chain"]
    evolution_chain_ids.append(extract_id_from_url(evolves_to["species"]["url"]))
    # Fetch other pokemons present in the chain as long as they exist.
    evolves_to = evolves_to["evolves_to"]
    while len(evolves_to) != 0:
        id = extract_id_from_url(evolves_to[0]["species"]["url"])
        # Fetch data about specific pokemon in the chain.
        evolution_chain_ids.append(id)
        evolves_to = evolves_to[0]["evolves_to"]
    # Return list with data about all pokemons in evelution chain.
    return get_pokemons_cached_data(user, evolution_chain_ids)
