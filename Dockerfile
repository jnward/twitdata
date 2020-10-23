FROM ubuntu:18.04

COPY . /home/twitxiv

WORKDIR /home/twitxiv

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    python3-pip \
    git

RUN pip3 install -r requirements.txt

ENV FLASK_APP=tweet_papers
ENV PYTHONPATH=/home/twitxiv

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN python3 tweet_papers/database/init_db.py

CMD python3 tweet_papers/database/populate.py & \
    flask run --host=0.0.0.0 --port=5000
