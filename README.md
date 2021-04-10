# twitXiv

https://twitxiv.jnward.me/

A simple webapp to aggrigate new scientific papers posted to Twitter.

### Usage:

1. Install the packages in `requirements.txt`
2. Set the environment variable `TWITTER_API_TOKEN` with your Twitter API token.
3. Initialize the database with `tweet_papers/database/init_db.py`
4. Populate the database with `tweet_papers/database/populate.py`
5. `flask run` from the `tweet_papers` directory, or use your favorite production server.