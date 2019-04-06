
import http.client
from flask_restplus import Namespace, Resource
from locations.db import db

ops_namespace = Namespace('ops', description='ops calls')


@ops_namespace.route('/healthcheck')
class HealthCheck(Resource):

    def get(self):
        '''
        Checks the app is running correctly
        '''
        try:
            db.session.execute('SELECT 1')
        except Exception as err:
            # Base except to capture any possible error
            msg = f'Cannot connect to DB: {err}'
            return msg, http.client.INTERNAL_SERVER_ERROR

        return 'All OK'
