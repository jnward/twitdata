import requests
import json

config = {
    'bearer_token': 'AAAAAAAAAAAAAAAAAAAAAA0HHwEAAAAAKScBILbQtnhkuRXlV3Zdw2ycS48%3DghnmP4cp4Wfgf53xOdW5GR5eOmr0bsHWJgDo\
579YdHE7KwLPO3'
}


class Tweet:

    def __init__(self, tweet_id, text=None, conversation_id=None, urls=[], author_data=None, quote_count=None, reply_count=None,
                 retweet_count=None, like_count=None, **kwargs):

        self.id = tweet_id
        self.text = text
        self.conversation_id = conversation_id
        self.urls = urls
        self.author_data = author_data
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.like_count = like_count

    def json(self):
        data = {
            'tweet_id': self.id,
            'text': self.text,
            'author_data': self.author_data,
            'conversation_id': self.conversation_id,
            'urls': self.urls,
            'quote_count': self.quote_count,
            'reply_count': self.reply_count,
            'retweet_count': self.retweet_count,
            'like_count': self.like_count
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
        pass  # TODO
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
        'expansions': 'author_id',
        'tweet.fields': 'public_metrics,referenced_tweets,conversation_id,entities',
        'user.fields': 'public_metrics,verified,name,username',
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


if __name__=='__main__':
    query = 'dataset -is:reply -is:retweet -is:quote lang:en has:links'
    tweets, next_token = query_recent(query, num_tweets=10)
    for i, tweet in enumerate(tweets):
        print(tweet.author_name)
        continue
        print(i, tweet.text)


