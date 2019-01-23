export FLASK_ENV='development'
export FLASK_APP=run.py
export DATABASE_URI="postgres://{user}@localhost:5432/{database}"
export TEST_DATABASE_URI="postgres://{user}@localhost:5432/{database}"
export SECRET_KEY="some secret key"