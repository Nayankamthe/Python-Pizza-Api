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
from your_app.models import db, User, Order

# Create the database tables (if they don't exist)
db.create_all()

# Access the Order and User models
orders = Order.query.all()
users = User.query.all()

# Display the results or perform any further actions
print("Orders:")
for order in orders:
    print(order)

print("Users:")
for user in users:
    print(user)
EOF
