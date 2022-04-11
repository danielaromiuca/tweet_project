import json
import logging
import time

import tweepy
from tweet_app.constants import BUCKET, PATH_TAGS_ECONOMIA, PREFIX_RAW_STREAM
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweet_app.utils import (
    API_ACCESS_TOKEN,
    API_ACCESS_TOKEN_SECRET,
    API_CONSUMER_KEY,
    API_CONSUMER_SECRET,
    get_full_text,
    get_ls_from_txt,
    tweets_to_s3,
)


class StdOutListener(StreamListener):
    def on_data(self, data):

        status_dict = json.loads(data)

        tweet = []  # List to add tweet fields

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
            tweets_to_s3(logger, BUCKET, PREFIX_RAW_STREAM, self.tweets)

            self.tweets = []

    def on_error(self, status):
        logger.error("There was a problem with the application: %s", status)


if __name__ == "__main__":

    tags_economia = get_ls_from_txt(PATH_TAGS_ECONOMIA)

    auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
    auth.set_access_token(API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET)

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/ec2-user/logs/stream.log",
    )
    logger = logging.getLogger("stream.log")

    l = StdOutListener()
    stream = Stream(auth, l, tweet_mode="extended")

    l.tweets = []  # New attribute to temp. store tweets

    try:
        logger.info("Launching streaming application")
        stream.filter(track=tags_economia)
    except tweepy.TweepError as e:
        logger.error("There was a problem with the application: %s", e)
        logger.info("Sleeping app for 90 secs. and trying to re launch")
        time.sleep(90)
        stream.filter(track=tags_economia)
