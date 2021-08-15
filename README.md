# Pokemon Webservice

Webservice about Pokemons that allows to create an account, browse all Pokemons, see details about them, add Pokemon to favorites.
Details about specific Pokemon: Name, Picture, Height, Weight, Stats, Abilities, and whole evolution chain.

## Tech stack
Application is built with Django and PostgreSQL. It benefits by PokeAPI (https://pokeapi.co/) wherefrom the data about every Pokemon is fetched.
Connection with API is made with Python's REQUESTS library (https://docs.python-requests.org/en/master/).

## How to run?

First of all, make sure that you have Docker installed.

- Clone this repo
- With code editor open `webservice/settings.py`
- At the top of this file find line `from .keys import DB_PASS` and comment it out
- In terminal hit `docker-compose run pokeserver`
- Close running process with `Ctrl + C`
- Run server with `docker-compose up`
- Open new terminal
- Go to the server container with `docker exec -it pokeserver bash`
- Migrate database with `python manage.py migrate`
- Run server with `py manage.py runserver`

Now you can open a browser on http://127.0.0.1:8000/, create an account and start browsing Pokemons!

You can find alternative way to run application without Docker [here]
You can preview the website [here]