import os
from flask import jsonify

# local imports
from app import create_app
from api.models.database import Migrate

config_name = os.getenv('FLASK_ENV', default='development')
app = create_app(config_name)
db = Migrate()


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to SendIT API'})


@app.cli.command()
def migrate():
    db.create_tables()


@app.cli.command()
def drop():
    db.drop_tables()
