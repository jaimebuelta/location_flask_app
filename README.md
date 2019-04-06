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
    $ docker-compose run test


Start the service locally
-----

Start the service with

    $ docker-compose up [-d] server

and access the service at `http://localhost:8080`. `-d` will run it as daemon and detach it from the terminal.

The service endpoints are documented in http://localhost:8080
