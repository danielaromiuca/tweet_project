import json
import logging
import time

import tweepy
from tweet_app.constants import BUCKET, PREFIX_RAW_SAMPLE
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweet_app.utils import (
    API_ACCESS_TOKEN,
    API_ACCESS_TOKEN_SECRET,
    API_CONSUMER_KEY,
    API_CONSUMER_SECRET,
    get_full_text,
    tweets_to_s3,
)


class StdOutListener(StreamListener):
    def __init__(self):
        self.tweets = []
        
    def on_data(self, data):

        status_dict = json.loads(data)

        tweet = []  # List to add tweet fields

        tweet.append("sample")
        tweet.append(str(status_dict.get("id")))
        tweet.append(get_full_text(status_dict))
        tweet.append(str(status_dict.get("created_at")))
        try:
            tweet.append(status_dict.get("user")["screen_name"])
        except TypeError:
            tweet.append(None)
        try:
            tweet.append(str(status_dict.get("user")["location"]))
        except TypeError:
            tweet.append(None)
        tweet.append(str(status_dict.get("coordinates")))
        tweet.append(str(status_dict.get("retweet_count")))
        tweet.append(str(status_dict.get("retweeted")))
        tweet.append(str(status_dict.get("source")))
        tweet.append(str(status_dict.get("favorite_count")))
        tweet.append(str(status_dict.get("favorited")))
        tweet.append(str(status_dict.get("in_reply_to_status_id_str")))

        self.tweets.append(tweet)

        if len(self.tweets) > 10000:
            logger.info("10000 mas!")
            tweets_to_s3(logger, BUCKET, PREFIX_RAW_SAMPLE, self.tweets)

            self.tweets = []

    def on_error(self, status):
        logger.error("There was a problem with the application: %s", status)


if __name__ == "__main__":

    auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
    auth.set_access_token(API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET)

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/ec2-user/logs/sample.log",
    )
    logger = logging.getLogger("sample.log")

    l = StdOutListener()
    stream = Stream(auth, l, tweet_mode="extended")

    try:
        logger.info("Launching sampling application")
        stream.sample()
    except tweepy.TweepError as e:
        logger.error("There was a problem with the application:  %s", e)
        logger.info("Sleeping app for 90 secs. and trying to re launch")
        time.sleep(90)
        stream.sample()
