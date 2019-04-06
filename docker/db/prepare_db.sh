#!/bin/sh
/opt/code/db/start_postgres.sh

echo 'Creating Schema'
python3 /opt/code/models.py

echo 'Loading initial data'

/opt/code/db/stop_postgres.sh
