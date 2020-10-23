from flask import render_template, jsonify
from twit_api import query_recent
from tweet_papers import app
from tweet_papers.database import Session
from tweet_papers.database.models import Tweet, TwitterUser, URL


print('def index')
@app.route('/')
def index():
    tweet_ids = get_tweet_ids(2)
    data = {'val': 'test_val',
            'tweet_ids': tweet_ids}
    return render_template('hello.html', data=data)


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
    print(next_token)
    tweet_ids = [tweet.id for tweet in tweets]
    print(tweet_ids)
    return tweet_ids, next_token


def get_tweets(num_ids=10, next_token=None):
    # keywords = "new newly build built building collect collected collecting develop developed developing research create created creating release released releasing arxiv".split()
    # keyword_str = "({})".format(" OR ".join(keywords))
    # query = f'dataset {keyword_str} -is:reply -is:retweet -is:quote lang:en has:links'
    query = '-is:reply -is:retweet -is:quote lang:en has:links (url:arxiv OR url:biorxicv OR url:medrxiv)'
    tweets, next_token = query_recent(query, num_tweets=num_ids, next_token=next_token)
    return tweets, next_token


@app.route('/query_tweets/<sort_by>')
def get_tweets_from_db(sort_by):
    print("Loading tweets with query:", sort_by)
    session = Session()
    tweets = session.query(Tweet)
    if sort_by == 'replies':
        tweets = tweets.order_by(Tweet.reply_count.desc())
    elif sort_by == 'retweets':
        tweets = tweets.order_by((Tweet.retweet_count + Tweet.quote_count).desc())
    else:
        tweets = tweets.order_by(Tweet.like_count.desc())
    tweets = tweets.limit(100).all()

    tweet_jsons = []
    for tweet in tweets:
        author = tweet.author
        urls = tweet.urls
        tweet_json = tweet.json()
        tweet_json['author_data'] = author.json()
        tweet_json['urls'] = [url.json() for url in urls]
        tweet_jsons.append(tweet_json)
    return jsonify(tweet_jsons)

