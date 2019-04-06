
from flask_restplus import Namespace, Resource

ops_namespace = Namespace('ops', description='ops calls')


@ops_namespace.route('/healthcheck')
class HealthCheck(Resource):

    def get(self):
        '''
        Checks the app is running correctly
        '''
        return 'All OK'
