from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitter_handle = db.Column(db.Unicode(140), unique=True, nullable=True)
    twitter_id = db.Column(db.Unicode(140), unique=True, nullable=True)
    twitter_access_token = db.Column(db.String(140), nullable=True)
    twitter_access_secret = db.Column(db.String(140), nullable=True)
    email = db.Column(db.String(40), nullable=True)
    name = db.Column(db.Unicode(140), nullable=True)
    profile_photo_url = db.Column(db.String(240), nullable=True)

class TwitterUser(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.Unicode(140), unique=True)
    name = db.Column(db.Unicode(240), unique=True)
    profile_image_url = db.Column(db.Text)

    @property
    def categories_q(self):
        return(db.session.query(Category)
               .join(UserCategory)
               .join(TwitterUser)
               .filter(UserCategory.category_id == self.id)
               )
        
    @property
    def categories(self):
        return [
            category.category
            for category in self.user_categories
        ]
    def __repr__(self):
        return f'<User {self.username}>'


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,
                        db.ForeignKey('twitter_user.id'),
                        nullable=False)
    user = db.relationship(
        'TwitterUser',
        backref=db.backref('tweets', lazy='dynamic'))
    text = db.Column(db.Unicode(500), nullable=False)
    embeddings = db.Column(db.PickleType, nullable=False)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Tweet {self.text}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(240), unique=True)

    @property
    def tweets_query(self):
        return (db.session.query(Tweet)
                .join(TwitterUser)
                .join(UserCategory)
                .filter(UserCategory.category_id == self.id)
                )
    @property
    def users_query(self):
        return (db.session.query(TwitterUser)
                .join(UserCategory)
                .filter(UserCategory.category_id == self.id)
                )
     
    @property
    def users(self):
        return [
            category.user
            for category in self.category_users
        ]
    
    def __repr__(self):
        return f'<Category {self.name}>'


class UserCategory(db.Model):
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False)
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=False)
    user = db.relationship(
        'TwitterUser', backref='user_categories')
    category = db.relationship(
        'Category', backref='category_users')

    __table_args__ = (
        db.UniqueConstraint('category_id', 'user_id', name='user_category_uc'),
        db.PrimaryKeyConstraint('category_id', 'user_id'),
        )

    def __repr__(self):
        return f'<CatI-DUserID {self.category_id} - {self.user_id}>'


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by_id = db.Column(db.BigInteger,
                              db.ForeignKey('user.id'),
                              nullable=False)
    final = db.Column(db.Boolean, default=False)
    created_by = db.relationship(
        'User', backref='games_created')
    datetime_created = db.Column(db.DateTime, server_default=db.func.now())


class TweetToGuess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer,
                        db.ForeignKey('game.id'),
                        nullable=False)

    tweet_id = db.Column(db.BigInteger,
                         db.ForeignKey('tweet.id'),
                         nullable=False)

    __table_args__ = (
        db.UniqueConstraint('game_id', 'tweet_id', name='game_tweet_uc'),
        )
    
    wrong_twitter_user1 = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=False)

    # In case we want to go multi-user
    wrong_twitter_user2 = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=True)

    wrong_twitter_user3 = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=True)
    wrong_twitter_user4 = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=True)

    wrong_twitter_user5 = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=True)


class GameParticipants(db.Model):
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)

    game_id = db.Column(
        db.Integer,
        db.ForeignKey('game.id'),
        nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            'user_id', 'game_id', name='game_participants_id'
        ),
        db.PrimaryKeyConstraint('user_id', 'game_id'),
    )


class Guess(db.Model):
    tweet_guess_id = db.Column(
        db.Integer,
        db.ForeignKey('tweet_to_guess.id'),
        nullable=False)
    guess_twitter_user_id = db.Column(
        db.BigInteger,
        db.ForeignKey('twitter_user.id'),
        nullable=False)
    user = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            'tweet_guess_id',
            'guess_twitter_user_id',
            'user', name='game_guesses'
        ),
        db.PrimaryKeyConstraint(
            'tweet_guess_id', 'guess_twitter_user_id', 'user'),
    )
