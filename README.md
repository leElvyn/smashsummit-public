# a public version of one of my web apps 

it's used for demonstration purposes, it comes with a websocket, and api to communicate with discord via an external bot views, a bit of frontend, and the really good django admin.

to launch with docker : 

you will need a psql database, setup the creds of the database in the docker-compose.yml and in the `smashsummit/settings.py`
then, just use docker-compose 


to launch with sqlite3 : 

install the deps with `pip ( pip3 for linux) install -r requirements.txt` 
the sqlite3 db inside the repo is already migrated, if you create a new one : `python manage.py migrate` (python3 for linux)

to start : 
```
python manage.py runserver
```
