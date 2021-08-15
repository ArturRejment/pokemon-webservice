Alternative way to run server without Docker

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