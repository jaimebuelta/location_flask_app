import os
from flask import Flask

from flask_restplus import Resource, Api

application = Flask(__name__)
api = Api(application, version='0.1', title='Locations API',
          description='A Simple CRUD API')


@api.route('/healthcheck')
class HealthCheck(Resource):

    def get(self):
        '''
        Checks the app is running correctly
        '''
        return 'All OK'
