import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/coolcodehack', methods=['POST'])
def expose():

    return json.dumps({"username": "snails", "password": "Come@snail2"})
