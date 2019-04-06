import os
from flask_sqlalchemy import SQLAlchemy

# Database initialisation
db_params = {
    'host': os.environ['POSTGRES_HOST'],
    'database': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'pwd': os.environ['POSTGRES_PASSWORD'],
    'port': os.environ['POSTGRES_PORT'],
}
DB_URI = 'postgresql://{user}:{pwd}@{host}:{port}/{database}'
db_config = {
    'SQLALCHEMY_DATABASE_URI': DB_URI.format(**db_params),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}
db = SQLAlchemy()
