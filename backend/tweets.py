import tweepy
from decouple import config
from .models import db, Tweet, TwitterUser, Category
import basilica
import flask
from sklearn.linear_model import LogisticRegression
APP = flask.current_app
TWITTER_AUTH = tweepy.OAuthHandler(
    config('TWITTER_CONSUMER_KEY'),
    config('TWITTER_CONSUMER_SECRET'),
)
TWITTER_AUTH.set_access_token(
    config('TWITTER_ACCESS_TOKEN'),
    config('TWITTER_ACCESS_TOKEN_SECRET'), 
)

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """Add or update user and tweets"""
    try:
        # Get twitter user from database or create a new user
        t_user = TWITTER.get_user(username)

        db_user = (
            TwitterUser.query.get(t_user.id) or
            TwitterUser(
                id=t_user.id, username=t_user.screen_name, name=t_user.name,
                profile_image_url=t_user.profile_image_url_https
                ))
        db.session.add(db_user)
        APP.logger.info(t_user)
        # get last tweet id and use it as a filter if exist
        last_tweet_id = \
            db_user.tweets.order_by(Tweet.id.desc()).first() or None
        last_tweet_id = last_tweet_id.id if last_tweet_id else None
        timeline = t_user.timeline(
            count=10000, exclude_replies=True,
            include_rts=False, tweet_mode='extended',
            since_id=last_tweet_id)
        # Basillica embeddings in a single API call
        if timeline:
            timeline_text, tweet_id, created_at = zip(
                *[(t.full_text, t.id, t.created_at)for t in timeline])
            embeddings = BASILICA.embed_sentences(
                timeline_text,
                model='twitter',
            )
            tweet_list = list(
                zip(tweet_id, timeline_text, embeddings, created_at))
            
            tweet_objects = [
                Tweet(id=t[0],
                      text=t[1][:500],
                      embeddings=t[2],
                      created_at=t[3])
                for t in tweet_list]
            
            db_user.tweets.extend(tweet_objects)
    except Exception as e:
        APP.logger.info(f'Error processing {username}')
        APP.logger.info(e)
        raise e
    else:
        db.session.commit()
    return db_user


def get_or_create_category(cat_name, cat_id=None):
    if cat_id:
        return Category.query.get(cat_id)
    category = Category.query.filter_by(name=cat_name).first() or\
        Category(name=cat_name)
    db.session.add(category)
    db.session.commit()
    return category
