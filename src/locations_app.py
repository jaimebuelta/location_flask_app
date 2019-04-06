from flask import Flask

from flask_restplus import Resource, Api

application = Flask(__name__)
api = Api(application)


@api.route('/healthcheck')
class HealthCheck(Resource):

    def get(self):
        '''
        Checks the app is running correctly
        '''
        return 'All OK'
