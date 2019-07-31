from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy, request
from flask_migrate import Migrate
import datetime
import os
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from .models import db, Tweet, TwitterUser, Category, UserCategory
from flask import jsonify, g
from .tweets import add_or_update_user, get_or_create_category
from .predict import predict_user
from authlib.flask.client import OAuth
from decouple import config
from .auth import AUTH, jwt_required,\
    JWT2, get_user_from_req
import random

def create_app():
    """
    App factory function
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'super secret key'
    db.init_app(app)
    app.register_blueprint(AUTH, url_prefix='/api/auth')
    migrate = Migrate(app, db)

    @app.route('/api/users', methods=['GET', 'POST'])
    @jwt_required(methods=['POST'])
    def users():
        user = None
        if request.method == 'POST':
            try:
                username = request.json['username']
                user = add_or_update_user(username)
            except Exception as e:
                response = jsonify({'error': str(e)})
                response.status_code = 500
                return response
            if request.json.get('cat_id'):
                category_id = request.json.get('cat_id')
                try:
                    user_category = UserCategory(
                        category_id=category_id, user_id=user.id)
                    db.session.add(user_category)
                    db.session.commit()
                except IntegrityError as e:
                    app.logger.info(e)
                    return jsonify({'error': 'User already in the category'})

        users = TwitterUser.query.all()
        users = [{'username': u.username, 'id': str(u.id),
                  'updated': u == user}
                 for u in users]
    
        return jsonify(users)

    @app.route('/api/user/<user_id>')
    def user_tweets(user_id):
        '''Get Tweets of the user'''
        user = TwitterUser.query.filter_by(id=user_id).first()
        tweets = \
            [t.text
             for t in user.tweets.order_by(Tweet.created_at.desc())]
        userObject = {'username': user.username, 'tweets': tweets}
        return jsonify(userObject)

    @app.route('/api/predict/<user1>/<user2>')
    def predict(user1, user2):
        '''predict who might've wrote the tweet'''
        tweet = request.args.get('tweet')
        winner = predict_user(user1, user2, tweet)
        return jsonify(winner.username)

    @app.route('/api/user_profile')
    @jwt_required()
    def user_profile():
        user = get_user_from_req(request)
        profile = {
            'user_name': user.twitter_handle,
            'photo_url': user.profile_photo_url
        }
        return jsonify(profile)

    @app.route('/api/categories', methods=['GET', 'POST'])
    @jwt_required(methods=['POST'])
    def categories():
        if request.method == 'POST':
            category = request.json
            get_or_create_category(category)
            try:
                category = request.json
                get_or_create_category(category)
            except Exception as e:
                response = jsonify({'error': str(e)})
                response.status_code = 500
                return response
        cats = Category.query.all()
        cat_dicts = [{'id': c.id, 'name': c.name} for c in cats]
        resp = jsonify(cat_dicts)
        return resp
   
    @app.route('/api/<user>/categories', methods=['GET', 'POST'])
    def user_categories(user):
        cats = TwitterUser.query.filter_by(username=user).first().categories
        cat_dicts = [{'id': c.id, 'name': c.name} for c in cats]
        resp = jsonify(cat_dicts)
        fake = jsonify([{'id': 1, 'name': 'whatever'}])
        return fake

    @app.route('/api/category/<category_id>/users', methods=['GET', 'POST'])
    def category_users(category_id):
        if request.method == 'POST':
            username = request.json
            user_obj = TwitterUser.query.filter_by(username=username).first()
            try:
                user_cat = UserCategory(category_id=category_id, user_id=user_obj.id)
                db.session.add(user_cat)
                db.session.commit()
            except IntegrityError as e:
                app.logger.info(e)
                return jsonify({'error': 'User already in the category'})

        users = Category.query.get(category_id).users
        users_dict = [{'id': u.id, 'name': u.username} for u in users]
        resp = jsonify(users_dict)
        return resp
    
    @app.route('/api/quickgame/<cat_id>/<count>', defaults={'options': '2'})
    @app.route('/api/quickgame/<cat_id>/<count>/<options>')
    def quickgame(cat_id, count, options):
        count = int(count)
        options = int(options)
        cat = Category.query.get(cat_id)
        tweets = cat.tweets_query.order_by(func.random()).limit(count).all()
        user_ids = [tweet.user_id for tweet in tweets]
        real_users = [TwitterUser.query.get(uid) for uid in user_ids]
        fake_users = []
        for tweet in tweets:
            fake_user = cat.users_query.filter(
                TwitterUser.id != tweet.user_id).order_by(func.random()).limit(options -1).all()
            fake_users.append(fake_user)
        game = zip(tweets, real_users, fake_users)
        
        game_list = [{'tweet': tweet.text, 'options': random.sample([
            *[{'handle': fake.username, 'name': fake.name,
              'photo': fake.profile_image_url, 'real': False}
              for fake in fakes],
            {'handle': real.username,
             'photo': real.profile_image_url,
             'name': real.name,
             'real': True}
        ], options)}
         for (tweet, real, fakes) in game]
        return jsonify(game_list)
    @app.route('/clear_db')
    def clear():
        db.drop_all()
        db.create_all()
        return 'ok'
    return app
