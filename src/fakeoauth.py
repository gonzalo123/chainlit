import logging

from flask import Flask, jsonify, make_response

from settings import SECRET, SESSION, DEBUG, JWT_EXPIRATION_TIMEDELTA, JWT_ALGORITHM
import jwt
from datetime import datetime

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET
app.config.update(SESSION)


@app.get(f"/oauth2/auth")
def auth():
    now = datetime.now()
    response = make_response(jsonify(dict(error='OK')), 200)
    expiration = now + JWT_EXPIRATION_TIMEDELTA
    user = 'gonzalo'
    display_name = 'Gonzalo'
    response.headers['X-User-JWT'] = str(jwt.encode(dict(
        user=user,
        display_name=display_name,
        exp=int(expiration.timestamp())
    ), SECRET, algorithm=JWT_ALGORITHM))
    logger.info("Fake OAuth authentication successful")
    return response
