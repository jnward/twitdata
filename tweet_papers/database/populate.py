from tweet_papers.views import query_recent
from tweet_papers.database import Session
from tweet_papers.database.models import Tweet, TwitterUser, URL
from datetime import datetime
import schedule
import time


def update_db(num_queries=450):
    query = '-is:reply -is:retweet -is:quote lang:en has:links url:arxiv'
    next_token = 'b26v89c19zqg8o3fos8uh240sf8nh52vb2dfluz3em6il'
    next_token = None
    queries = 0
    while queries < num_queries:
        print(f'Updating database ... running query {queries+1} with next_token {next_token}')
        tweets, next_token = query_recent(query, num_tweets=100, next_token=next_token)
        push_to_db(tweets)
        queries += 1
        if next_token is None:
            break


def push_to_db(tweets):
    session = Session()

    for tweet in tweets:
        author_data = tweet.author_data
        user_obj, is_new = TwitterUser.get_or_create(session=session, user_id=author_data['id'], **author_data, **author_data['public_metrics'])
        if not is_new:
            for key, value in author_data.items():
                setattr(user_obj, key, value)
        session.add(user_obj)
        session.commit()

    for tweet in tweets:  # can bulk add tweets for slight speedup
        tweet_data = tweet.json()
        author_data = tweet.author_data
        tweet_obj, is_new = Tweet.get_or_create(session=session, **tweet_data, author_id=author_data['id'])
        if not is_new:
            for key, value in tweet_data.items():
                if key == 'created_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                elif key == 'urls':
                    continue
                setattr(tweet_obj, key, value)
        else:
            urls = tweet_data['urls']
            for url in urls:
                url_obj = URL(tweet.id, **url)
                session.add(url_obj)
        session.add(tweet_obj)
    session.commit()


if __name__ == '__main__':
    schedule.every(30).minutes.do(update_db)
    while True:
        schedule.run_pending()
        time.sleep(60)
