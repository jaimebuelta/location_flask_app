import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_restplus import Resource, Api

application = Flask(__name__)
api = Api(application)

# Database initialisation
db_params = {
    'host': os.environ['POSTGRES_HOST'],
    'database': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'pwd': os.environ['POSTGRES_PASSWORD'],
    'port': os.environ['POSTGRES_PORT'],
}
DB_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{database}'
application.config['SQLALCHEMY_DATABASE_URI'] = DB_URI.format(**db_params)
db = SQLAlchemy(application)


@api.route('/healthcheck')
class HealthCheck(Resource):

    def get(self):
        '''
        Checks the app is running correctly
        '''
        return 'All OK'
