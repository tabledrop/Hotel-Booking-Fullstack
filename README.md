# Hotel Booking Fullstack

This is the first project for the CSCI 440 class at TAMUC

To use, install Flask and its dependencies for Python by running:

```
$ pip install -r requirements.txt
```

To run webserver do:

```
$ python app.py
```

By default, the script will run in debug mode as `app.run(debug=TRUE)` flag is set. The console should also output database activity whenever appropriate

If you keep encountering a "server overloaded" error when creating the account, ensure that the database is migrated according to the classes as defined in `app.py`. To do this run:

```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
