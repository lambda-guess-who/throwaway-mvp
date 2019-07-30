from flask import Blueprint, request, jsonify, abort
import flask
from authlib.client import OAuth1Session
import redis
from decouple import config
import tweepy
import json
from authlib.jose import jwt
import datetime
from .models import User, db
from functools import wraps


AUTH = Blueprint('auth', __name__)
REDIS_URL_STRING = config('REDIS_URL')
R = redis.Redis.from_url(REDIS_URL_STRING)
APP = flask.current_app

class JWTHS256():
    def __init__(self, key, iss):
        self.key = key
        self.header = {'alg': 'HS256'}
        self.iss = iss
    
    def encode(self, payload):
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        new_payload = {
            'iat': int(now.timestamp()),
            'exp': int(tomorrow.timestamp()),
            'iss': self.iss
        }
        new_payload.update(payload)
        header = self.header
        key = self.key
        APP.logger.info(header)
        APP.logger.info(new_payload)
        APP.logger.info(key)
        return jwt.encode(header, new_payload, key)

    def decode(self, data_string):
        return jwt.decode(data_string, self.key)

JWT2 = JWTHS256(config('HS256_KEY'), 'Guess Who?')

@AUTH.route('/create_login_url', methods=['GET', 'POST'])
def create_login_url():
    
    if request.method == 'POST':
        nonce = request.json.get('nonce')
        callback_url = request.json.get('callback_url')
        APP.logger.info(REDIS_URL_STRING)
        auth = tweepy.OAuthHandler(
            config('TWITTER_CONSUMER_KEY'),
            config('TWITTER_CONSUMER_SECRET'),
            callback_url
        )
        try:
            redirect_url = auth.get_authorization_url()
            auth_token_json = json.dumps(auth.request_token)
            R.set(nonce, auth_token_json, ex=180)
        except tweepy.TweepError:
            APP.logger.info('Failed to get request token')
        return jsonify({'redirect_url': redirect_url})
    return 'ok'


@AUTH.route('/verify_login', methods=['GET', 'POST'])
def verify_login_url():
    APP = flask.current_app
    if request.method == 'POST':
        auth = tweepy.OAuthHandler(
            config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET'))
        nonce = request.json.get('nonce')
        verifier = request.json.get('verifier')
        token = json.loads(R.get(nonce))
        auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        APP.logger.info('Error! Failed to get access token.')
    api = tweepy.API(auth)
    APP.logger.info(auth.access_token)
    APP.logger.info(auth.access_token_secret)
    user = api.verify_credentials(include_email='true', skip_status='true')._json
    twitter_handle = user.get('screen_name')
    twitter_id = user.get('id_str')
    twitter_access_token = auth.access_token
    twitter_access_secret = auth.access_token_secret
    email = user.get('email')
    name = user.get('name')
    profile_photo_url = user.get('profile_image_url_https')
    db_user = (
        User.query.filter_by(twitter_id=twitter_id).first() or
        User(twitter_handle=twitter_handle,
             twitter_id=twitter_id,
             twitter_access_token=twitter_access_token,
             twitter_access_secret=twitter_access_secret,
             email=email,
             name=name,
             profile_photo_url=profile_photo_url)
               )
    APP.logger.info(db_user)
    APP.logger.info(user)
    db.session.add(db_user)
    db.session.commit()
    jwt2 = JWTHS256(config('HS256_KEY'), 'Guess Who?')
    jwt_string = jwt2.encode({'userID': db_user.id})
    APP.logger.info(jwt_string)
    return jsonify({'jwt': jwt_string.decode('utf-8')})


def jwt_required(methods=('GET', 'POST',)):
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            if request.method not in methods:
                return f(*args, **kwargs)
            auth_header = request.headers.get('Authorization')
            if auth_header:
                _, jwt_token = auth_header.split(' ')
                claims = JWT2.decode(jwt_token)
                try:
                    claims.validate()
                except:
                    resp = jsonify({'error': 'Cannot verify user'})
                    resp.status_code = 401
                    return resp
                return f(*args, **kwargs)
            else:
                resp = jsonify({'error': 'Cannot verify user'})
                resp.status_code = 401
                return resp
        return func
    
    return decorator

def get_user_from_req(req):
    auth_header = req.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        claims = JWT2.decode(auth_token)
        user = User.query.get(claims['userID'])
        return user
    else:
        abort(401)