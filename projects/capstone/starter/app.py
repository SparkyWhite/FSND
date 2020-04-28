import os
from flask import Flask, request, jsonify, abort
#from sqlalchemy import exc
import json
from flask_cors import CORS
#from .database.models import setup_db
from models import setup_db

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def generic():
        return "I'm a basic application"

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)