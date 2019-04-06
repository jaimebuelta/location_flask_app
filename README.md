Locations app
========

A RESTful app to track location of products


Requirements
-----

Install [docker-compose](https://docs.docker.com/compose/install/)


Run tests
-----

The unit-tests are available in the `./tests` subdirectory

Call

    $ docker-compose build test
    $ docker-compose up test

Note this will keep the db between test executions. If you want to recreate the db from scratch, do

    $ docker-compose up --build test

Which will recreate all the dependencies, including the db. For code changes, it's not necessary.


Start the service locally
-----

Start the service with

    $ docker-compose up [--build] [-d] server

and access the service at `http://localhost:8080`. `-d` will run it as daemon and detach it from the terminal. `--build` will rebuild the service and all its dependencies (including the db)

The service endpoints are documented in http://localhost:8080


Comments
------

The API is divided in two, an ops endpoint, that contains the healthcheck, and the api namespace that contains the service. The healthcheck checks that the connection with
the DB works fine, as well as the service is up and running.

The api has two main entities, products and locations. Locations are associated to products. The timestamp is generated automatically by the server, and locations cannot be edited. This is to protect with tampering on the locations, as changing later when a product was in a particular place (or the place) seems not required. A possibility may be that the product accumulate positions to send to the remote server at a later stage. In any case, the application could be changed.
Products are changeable, and removable. Deleting a product deletes all its locations automatically.
Both Products and Locations are stored in two tables in the DB. The model is quite straigthforward. The only caveat is to store longitude and latitude as floats, which may lose precission if there's later some arithmetic done. There are specific GIS fields to store geolocation in various DBS (including PostgreSQL), but I thought not to go that route unless there's a requirement. The elevation is stored as an integer, which gives a resolution of 1m. All times are stored in UTC.

The tech stack used is Flask, with Flask-RESTPlus as the main framework, as it generates automatically a swagger interface that makes the discovery of the API very easy. The connection to the PostgreSQL DB uses SQLAlchemy. The tests run with pytest.

To generate the environment, I've used docker and docker-compose. The basis for that a template I generated, available [in GitHub](https://github.com/jaimebuelta/django-docker-template), though I've updated some things. The template is more complete in terms of :prod-readiness" (logs, metrics, etc), and there has been changed based on next things I've learn the last year. (I should update the template, there are some things I learnt recently, like multi-stage docker builds that are great). The template is also based in Django, not Flask.
Even not taking into account the production advantages of docker, it works as a way of creating an extra layer to ensure that it runs smoothly no matter where, sort of a super-virtualenv.

The initial data is stored in the file `docker/db/input.txt` and gets uploaded at the start of the creation of the DB, just after the schema creation. This happens in the script `src/load_from_csv.py`. As a curiosity, given that we upload rows defining spefic primary keys, then we need to update the sequence to not have later issues with primary key reusage. This is a peculiarity of PostgreSQL that has bitten me a few times.

The only API that is paginated is the "all locations" one, that returns the data in a format similar to the one in input.txt. This is the view that has the most number of elements. If could be added to the other endpoints as well.

I tried to include some interesting techniques in testing, like parametrising some tests, freeze the time, mocking a DB call or creating pytest fixtures. Most of the test are done from an API perspective, which I think is what makes most sense for these services. Where there's a specific function or module that can be good to test on its own, it can also be done (e.g. `get_next_page` and `get_previous_page`)
