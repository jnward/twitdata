from flask import render_template, jsonify
from twit_api import query_recent
from tweet_papers import app
from tweet_papers.database import Session
from tweet_papers.database.models import Tweet, TwitterUser, URL
from werkzeug.utils import import_string
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'filesystem',
                           'CACHE_DIR': "./tweet_papers/cache/",
                           'CACHE_THRESHOLD': 1000000})


@app.route('/')
def index():
    return render_template('hello.html', data={})


#@app.route('/load_tweets/<next_token>')
def load_tweets(next_token):
    print("Loading tweets with next_token:", next_token)
    if next_token == 'head':
        next_token = None
    tweets, next_token = get_tweets(100, next_token)
    if next_token is None:
        next_token = 'end'
    data = {'tweets_data': [tweet.json() for tweet in tweets],
            'next_token': next_token}
    return jsonify(data)


def get_tweet_ids(num_ids=10, next_token=None):
    query = 'dataset -is:reply -is:retweet -is:quote lang:en has:links'
    tweets, next_token = query_recent(query, num_tweets=num_ids, next_token=next_token)
    tweet_ids = [tweet.id for tweet in tweets]
    return tweet_ids, next_token


def get_tweets(num_ids=10, next_token=None):
    # keywords = "new newly build built building collect collected collecting develop developed developing research create created creating release released releasing arxiv".split()
    # keyword_str = "({})".format(" OR ".join(keywords))
    # query = f'dataset {keyword_str} -is:reply -is:retweet -is:quote lang:en has:links'
    query = '-is:reply -is:retweet -is:quote lang:en has:links (url:arxiv OR url:biorxicv OR url:medrxiv)'
    tweets, next_token = query_recent(query, num_tweets=num_ids, next_token=next_token)
    return tweets, next_token


@app.route('/query_tweets/<sort_by>')
@cache.cached(timeout=3600)
def get_tweets_from_db(sort_by):
    print("Loading tweets with query:", sort_by)
    session = Session()
    tweets = session.query(Tweet, TwitterUser, URL).join(TwitterUser).join(URL)
    if sort_by == 'replies':
        tweets = tweets.order_by(Tweet.reply_count.desc())
    elif sort_by == 'retweets':
        tweets = tweets.order_by((Tweet.retweet_count + Tweet.quote_count).desc())
    else:
        tweets = tweets.order_by(Tweet.like_count.desc())
    tweets = tweets.limit(100).all()
    tweet_jsons = {}
    for tweet, author, url in tweets:
        tweet_json = tweet.json()
        tweet_json['author_data'] = author.json()
        tweet_jsons[tweet.id] = tweet_json
        if tweet_jsons[tweet.id].get('urls') is not None:
            tweet_jsons[tweet.id]['urls'] += url.json()
        else:
            tweet_jsons[tweet.id]['urls'] = [url.json()]
    return jsonify(list(tweet_jsons.values()))

