# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, String, Integer, BigInteger, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from tweet_papers.database.db import Base
from datetime import datetime


class TwitterUser(Base):
    __tablename__ = "twitter_user"
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String)
    name = Column(String)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    tweet_count = Column(Integer)
    listed_count = Column(Integer)

    def __init__(self, user_id, username=None, name=None, followers_count=None, following_count=None,
                 tweet_count=None, listed_count=None, **kwargs):
        self.id = str(user_id)
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.tweet_count = tweet_count
        self.listed_count = listed_count

    def __repr__(self):
        return f'<TwitterUser {self.id}>'

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = session.query(cls).get(kwargs['user_id'])
        if instance:
            return instance, False
        else:
            instance = cls(**kwargs)
            session.add(instance)
            return instance, True

    def json(self):
        data = {
            'id': str(self.id),
            'username': self.username,
            'name': self.name,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'tweet_count': self.tweet_count,
            'listed_count': self.listed_count
        }
        return data


class Tweet(Base):
    __tablename__ = "tweet"
    id = Column(Text, primary_key=True, autoincrement=False)
    author_id = Column(Integer, ForeignKey('twitter_user.id'))
    text = Column(String)
    retweet_count = Column(Integer)
    reply_count = Column(Integer)
    like_count = Column(Integer)
    quote_count = Column(Integer)
    created_at = Column(DateTime)
    retweeted = Column(Boolean, default=False)

    urls = relationship("URL", backref="tweet")
    author = relationship("TwitterUser", backref="tweets")

    def __init__(self, tweet_id, author_id=None, text=None, retweet_count=None, reply_count=None, like_count=None,
                 quote_count=None, created_at=None, **kwargs):
        self.id = str(tweet_id)
        self.author_id = author_id
        self.text = text
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count
        if isinstance(created_at, datetime):
            self.created_at = created_at
        elif isinstance(created_at, str):
            self.created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self.created_at = None

    def __repr__(self):
        return f'<Tweet {self.id}>'

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = session.query(cls).get(kwargs['id'])
        if instance:
            return instance, False
        else:
            instance = cls(kwargs.get('id'), **kwargs)
            session.add(instance)
            return instance, True

    def json(self):
        data = {
            'id': str(self.id),
            'author_id': str(self.author_id),
            'text': self.text,
            'retweet_count': self.retweet_count,
            'reply_count': self.reply_count,
            'like_count': self.like_count,
            'quote_count': self.quote_count,
            'created_at': str(self.created_at)
        }
        return data


class URL(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey('tweet.id'))
    start = Column(Integer)
    end = Column(Integer)
    url = Column(String(512))
    expanded_url = Column(String(512))
    display_url = Column(String(512))

    def __init__(self, tweet_id, start, end, url, expanded_url, display_url, **kwargs):
        self.tweet_id = tweet_id
        self.start = start
        self.end = end
        self.url = url
        self.expanded_url = expanded_url
        self.display_url = display_url

    def __repr__(self):
        return f'<URL {self.expanded_url}>'

    def json(self):
        data = {
            'id': self.id,
            'tweet_id': self.tweet_id,
            'start': self.start,
            'end': self.end,
            'url': self.url,
            'expanded_url': self.expanded_url,
            'display_url': self.display_url
        }
        return data

