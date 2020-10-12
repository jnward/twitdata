from flask import render_template, Flask, jsonify
from twit_api import query_recent


app = Flask(__name__, template_folder='static/html')


@app.route('/')
def index():
    tweet_ids = get_tweet_ids(2)
    data = {'val': 'test_val',
            'tweet_ids': tweet_ids}
    return render_template('hello.html', data=data)


@app.route('/load_tweets/<next_token>')
def load_tweets(next_token):
    print("Loading tweets with next_token:", next_token)
    if next_token == 'head':
        next_token = None
    tweets, next_token = get_tweets(10, next_token)
    if next_token is None:
        next_token = 'end'
    data = {'tweets_data': [tweet.json() for tweet in tweets],
            'next_token': next_token}
    print(data)
    return jsonify(data)


def get_tweet_ids(num_ids=10, next_token=None):
    query = 'dataset -is:reply -is:retweet -is:quote lang:en has:links'
    tweets, next_token = query_recent(query, num_tweets=num_ids, next_token=next_token)
    print(next_token)
    tweet_ids = [tweet.id for tweet in tweets]
    print(tweet_ids)
    return tweet_ids, next_token


def get_tweets(num_ids=10, next_token=None):
    query = 'dataset -is:reply -is:retweet -is:quote lang:en has:links'
    tweets, next_token = query_recent(query, num_tweets=num_ids, next_token=next_token)
    return tweets, next_token





