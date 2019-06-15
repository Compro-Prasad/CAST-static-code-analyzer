## Static Code Analyzer backend

Make sure you are in the `backend/` directory before executing the following
commands.

### Initial Setup

```
cp .env.example .env
```

Fill in the MySQL db details in `.env` file.

Make sure you have `pipenv` installed on your system. Else you can also make
your own virtualenv.

```
pipenv --three # Creates virtualenv
pipenv shell   # activates virtualenv
pip install -r requirements.txt
python3 manage.py migrate # Creates tables in db
```

### Starting the server

Everytime before starting the server you need to activate virtual environment
using `pipenv shell`. Then just run:

```
./manage.py runserver
```

Or if you want to make it available in the whole network use:

```
./manage.py runserver 0.0.0.0:8000
```
