"""Gets user timelines."""
import logging
import random
import time as tm

import tweepy
from constants import BUCKET, PATH_USER_LIST, PREFIX_RAW_TIMELINE
from utils import (
    API_ACCESS_TOKEN,
    API_ACCESS_TOKEN_SECRET,
    API_CONSUMER_KEY,
    API_CONSUMER_SECRET,
    get_ls_from_txt,
    tweets_to_s3,
)

if __name__ == "__main__":

    auth = tweepy.OAuthHandler(API_CONSUMER_KEY, API_CONSUMER_SECRET)
    auth.set_access_token(API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True
    )

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="/home/ec2-user/logs/timeline.log",
    )
    logger = logging.getLogger("timeline.log")

    user_list = get_ls_from_txt(PATH_USER_LIST)

    tweets = []

    while True:

        user = random.choice(user_list)

        try:
            for page in tweepy.Cursor(
                api.user_timeline,
                screen_name=user,
                exclude_replies=False,
                tweet_mode="extended",
                count=3200,
            ).pages():
                tm.sleep(1)

                logger.info("Tweets recovered for user: %s, %s", user, str(len(page)))

                for status in page:

                    tweet = []  # List to add tweet fields

                    tweet.append(str(status.get("id")))
                    tweet.append(str(status.get("full_text")))
                    tweet.append(str(status.get("created_at")))
                    try:
                        tweet.append(status.get("user")["screen_name"])
                    except AttributeError:
                        tweet.append(None)
                    try:
                        tweet.append(str(status.get("user")["location"]))
                    except AttributeError:
                        tweet.append(None)
                    tweet.append(str(status.get("coordinates")))
                    tweet.append(str(status.get("retweet_count")))
                    tweet.append(str(status.get("retweeted")))
                    tweet.append(str(status.get("source")))
                    tweet.append(str(status.get("favorite_count")))
                    tweet.append(str(status.get("favorited")))
                    tweet.append(str(status.get("in_reply_to_status_id_str")))

                    tweets.append(tweet)

                    if len(tweets) > 20000:

                        tweets_to_s3(logger, BUCKET, PREFIX_RAW_TIMELINE, tweets)

                        tweets = []

        except tweepy.TweepError as e:
            logger.error("Error getting Tweets for user: %s. Error msg.: %s", user, e)
