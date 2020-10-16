from tweet_papers.database.db import Base, Session, engine
from tweet_papers.database.models import Tweet, TwitterUser

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)  # create db
