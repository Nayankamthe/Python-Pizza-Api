#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cmd /c env\\Scripts\\activate

export FLASK_APP=runserver.py

flask shell <<EOF

db
User
Order
db.create_all()

