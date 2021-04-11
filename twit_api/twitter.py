import requests
import os
from requests_oauthlib import OAuth1Session



config = {
    'bearer_token': os.getenv('TWITTER_BEARER_TOKEN'),
    'consumer_key': os.getenv('TWITTER_CONSUMER_KEY'),
    'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET'),
    'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
    'token_secret': os.getenv('TWITTER_SECRET_TOKEN'),
}


class Tweet:

    def __init__(self, tweet_id, text=None, conversation_id=None, urls=[], author_data=None, quote_count=None, reply_count=None,
                 retweet_count=None, like_count=None, created_at=None, **kwargs):

        self.id = tweet_id
        self.text = text
        self.conversation_id = conversation_id
        self.urls = urls
        self.author_data = author_data
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.like_count = like_count
        self.created_at = created_at

    def json(self):
        data = {
            'id': self.id,
            'text': self.text,
            'author_data': self.author_data,
            'conversation_id': self.conversation_id,
            'urls': self.urls,
            'quote_count': self.quote_count,
            'reply_count': self.reply_count,
            'retweet_count': self.retweet_count,
            'like_count': self.like_count,
            'created_at': str(self.created_at)
        }

        return data


def parse_response(response_json):
    tweets = []
    data = response_json.get('data')
    if not data:
        return []
    try:
        users = response_json['includes']['users']
    except KeyError:
        user_dict = {}
    else:
        user_dict = {user['id']: user for user in users}
    for tweet in data:
        #print(tweet['truncated'])
        tweet_metrics = tweet.get('public_metrics')
        referenced_tweets = tweet.get('referenced_tweets', [])
        tweet_id = tweet['id']
        author_id = tweet['author_id']
        text = tweet['text']
        conversation_id = tweet['conversation_id']
        created_at = tweet['created_at']
        author_data = user_dict.get(tweet['author_id'])
        # print(author)
        # author_name = author.get('name') if author else ''
        # author_username = author.get('username') if author else ''
        # author_metrics = author.get('public_metrics') if author else {}
        # author_data = {
        #     'id': author_id,
        #     'name': author_name,
        #     'username': author_username,
        #     'metrics': author_metrics
        # }
        entities = tweet.get('entities', {})
        urls = entities.get('urls')
        tweet_obj = Tweet(
            tweet_id,
            text,
            conversation_id,
            urls,
            author_data,
            created_at = created_at,
            **tweet_metrics,
        )
        tweets.append(tweet_obj)
    return tweets


def _query_recent_with_next(params, next_token=None):
    url = "https://api.twitter.com/2/tweets/search/recent"
    bearer_token = config.get('bearer_token')
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }
    if next_token is not None:
        params['next_token'] = next_token
    res = requests.get(url, headers=headers, params=params)
    if not res.status_code == 200:
        print(res.status_code)
        print(res.text)
        pass  # TODO 503 etc
    try:
        output = res.json()
    except AttributeError as e:
        print(res.text)
        print(e)
        return {}, 403
    try:
        next_token = output['meta']['next_token']
    except KeyError:
        next_token = None
    parsed = parse_response(output)
    return parsed, next_token


def query_recent(query, num_tweets=1, next_token=None):
    # next_token = None
    tweets = []
    end = False
    params = {
        'query': query,
        'expansions': 'author_id,attachments.media_keys',
        'tweet.fields': 'public_metrics,referenced_tweets,conversation_id,entities,created_at',
        'user.fields': 'public_metrics,verified,name,username',
        'media.fields': 'preview_image_url,public_metrics',
    }
    for i in range(num_tweets//100):
        params['max_results'] = 100
        cur, next_token = _query_recent_with_next(params, next_token)
        tweets.extend(cur)
        if next_token is None:
            end = True
            break
    if num_tweets%100 and not end:
        params['max_results'] = max(num_tweets%100, 10)
        cur, next_token = _query_recent_with_next(params, next_token)
        tweets.extend(cur)
    return tweets[:num_tweets], next_token


def retweet(tweet_id):
    consumer_key = config.get('consumer_key')
    consumer_secret = config.get('consumer_secret')
    access_token = config.get('access_token')
    token_secret = config.get('token_secret')
    twitter_sess = OAuth1Session(client_key=consumer_key,
                                 client_secret=consumer_secret,
                                 resource_owner_key=access_token,
                                 resource_owner_secret=token_secret)
    url = f"https://api.twitter.com/1.1/statuses/retweet/{tweet_id}.json"

    res = twitter_sess.post(url)
    if not res.status_code == 200:
        print(res.status_code)
        print(res.text)
        return False
    return True


if __name__=='__main__':
    # query = 'dataset -is:reply -is:retweet -is:quote lang:en has:links'
    # tweets, next_token = query_recent(query, num_tweets=100)
    # for i, tweet in enumerate(tweets):
    #     print(i, tweet.json())

    res = retweet(21)
    print(res)


