from tweet_papers.database import Session
from tweet_papers.database.models import Tweet
from twit_api import retweet

def retweet_top_unretweeted():
	session = Session()
	q = session.query(Tweet).filter(Tweet.retweeted==False).order_by(Tweet.like_count.desc())
	tweet = q.first()
	print(tweet)
	if tweet is None:
		return
	retweet(tweet.id)
	tweet.retweeted=True
	session.add(tweet)
	session.commit()


if __name__ == '__main__':
    retweet_top_unretweeted()
    schedule.every(2).hours.do(retweet_top_unretweeted)
    while True:
        schedule.run_pending()
        time.sleep(600)
