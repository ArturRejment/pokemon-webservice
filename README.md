# Pokemon Webservice

Webservice about Pokemons that allows to create an account, browse all Pokemons, see details about them, add Pokemon to favorites.
Details about specific Pokemon: Name, Picture, Height, Weight, Stats, Abilities, and whole evolution chain.

## Tech stack
Application is built with Django and PostgreSQL. It benefits by PokeAPI (https://pokeapi.co/) wherefrom the data about every Pokemon is fetched.
Connection with API is made with Python's REQUESTS library (https://docs.python-requests.org/en/master/). Fetched pokemon data is cached with Redis database in order to improve application performance. Whole application is containerized with Docker. Django, Postgres and Redis are connected by the use of docker-compose.

## How to run?

First of all, make sure that you have Docker installed.

- Clone this repo
- Run server with `docker-compose up`

Now you can open a browser on http://127.0.0.1:8000/, create an account and start browsing Pokemons!

You can find alternative way to run application without Docker [here](https://github.com/ArturRejment/pokemon-webservice/blob/main/docs/alternative.md).

You can preview the website [here](https://github.com/ArturRejment/pokemon-webservice/blob/main/docs/preview.md).
