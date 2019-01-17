import os
from flask import jsonify

# local imports
from app import create_app
from config import config

config_name = os.getenv('FLASK_CONFIG_ENV', default='development')
app = create_app(config[config_name])


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to SendIT API'})


if __name__ == '__main__':
    app.run(debug=True)
