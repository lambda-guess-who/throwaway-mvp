import numpy as np
from sklearn.linear_model import LogisticRegression
from.models import TwitterUser
from.tweets import BASILICA

def predict_user(u1,u2, tweet_text):
    '''unused code for prediction'''
    user1 = TwitterUser.query.filter_by(id=u1).one()
    user2 = TwitterUser.query.filter_by(id=u2).one()
    user1_embeddings = np.array([t.embeddings for t in user1.tweets])
    user2_embeddings = np.array([t.embeddings for t in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.zeros(user1.tweets.count()),
                             np.ones(user2.tweets.count())])
    log_reg = LogisticRegression().fit(embeddings, labels)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    results = log_reg.predict(np.array(tweet_embedding).reshape(1,-1))[0]
    result_summary = [user1, user2][int(results)]
    return result_summary
