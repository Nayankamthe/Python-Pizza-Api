#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Activating python environment"
echo
echo "###########################################################################################"
# Activate the virtual environment
source env/Scripts/activate
echo "Activating python environment Completed..!"
echo
echo "###########################################################################################"
echo "Installing Python requirements.txt"
echo
echo "###########################################################################################"
# Install packages
pip install -r requirements.txt
echo "Installing package of Python requirements.txt completed..!"
echo
echo "###########################################################################################"

echo "exporting FLASK_APP= runserver.py"
# Set FLASK_APP environment variable
export FLASK_APP=runserver.py
echo "exporting FLASK_APP= runserver.py completed..!"

# # Start the Gunicorn server for your Flask app
# gunicorn runserver:app &

# # Sleep for a moment to allow Gunicorn to start (adjust the time as needed)
# sleep 10
echo "Started database migration using flask shell"
# Start Flask shell and run individual commands
flask shell <<EOF

db
db.create_all()
EOF

echo "database model migration completed..!"
echo
echo "###########################################################################################"
echo "Returning to the main build script..."
echo
echo "###########################################################################################"

echo "Checking tables using flask shell"
echo "###########################################################################################"
echo
# Start Flask shell and run individual commands
flask shell <<EOF
print("Order url:$Order")
Order.query.all()
print("User url :$User")
User.query.all()

EOF
echo
echo "###########################################################################################"