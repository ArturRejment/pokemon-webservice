# Pokemon Webservice

Webservice about Pokemons that allows to create an account, browse all Pokemons, see details about them, add Pokemon to favorites.
Details about specific Pokemon: Name, Picture, Height, Weight, Stats, Abilities, and whole evolution chain.

## Tech stack
Application is built with Django and PostgreSQL. It benefits by PokeAPI (https://pokeapi.co/) wherefrom the data about every Pokemon is fetched.
Connection with API is made with Python's REQUESTS library (https://docs.python-requests.org/en/master/).

## How to run?

- Clone this repo and open its directory in terminal
- Create a new virtual environment with `py -m venv env`
- Activate virtual environment with `env\Scripts\activate.bat`
- Install necessary libraries with `pip install -r requirements.txt`
- Create locally new Postgres database
- With code editor open `webservice/settings.py`
- Find a dictionary named `DATABASES` and change credentials to match with your database
- At the top of this file find line `from .keys import DB_PASS` and comment it out
- Migrate models to the database with `py manage.py migrate`
- Run server with `py manage.py runserver`

Now you can open a browser on http://127.0.0.1:8000/, create an account and start browsing Pokemons!
