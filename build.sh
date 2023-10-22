#!/usr/bin/env bash
# exit on error
set -o errexit

# Activate the virtual environment
source env/Scripts/activate

# Install packages
pip install -r requirements.txt
# Set FLASK_APP environment variable
export FLASK_APP=runserver.py

# # Start the Gunicorn server for your Flask app
# gunicorn runserver:app &

# # Sleep for a moment to allow Gunicorn to start (adjust the time as needed)
# sleep 10

# Start Flask shell and run individual commands
flask shell <<EOF

db
User
Order
db.create_all()

EOF
