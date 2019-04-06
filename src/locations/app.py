from flask import Flask

from flask_restplus import Api
from locations.api_namespace import api_namespace
from locations.ops_namespace import ops_namespace

application = Flask(__name__)
api = Api(application, version='0.1', title='Locations API',
          description='A Simple CRUD API')

api.add_namespace(ops_namespace)
api.add_namespace(api_namespace)
