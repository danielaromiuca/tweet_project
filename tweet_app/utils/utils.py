"""Auxiliary functions."""
from datetime import datetime

import pandas as pd


def get_ls_from_txt(path):  # Modificar!!! Que lea txt y devuelva lista!!!
    """Get a list from a txt file.

    Reads a txt file and returns a list of str.

    Parameters
    ----------
        path: str
            absolute path to the text file
    Returns
    -------
        list:
            list of strings"""
    with open(path, "r") as file:
        tags = file.read().splitlines()
    return tags


def get_full_text(status):
    """Get a full text from a tweet received using stream API.

    Parameters
    ----------
        status: json
            json object with the parsed data receved from the API
    Returns
    -------
        str:
            if available, the extended tweet text.
            if not available, the text of the regular tweet.
            if that is not available, None"""
    if hasattr(status, "extended_tweet"):
        return status.extended_tweet["full_text"]
    return status.get("text")


def tweets_to_s3(logger, bucket, prefix, tweets):
    """Upload the tweets to S3 in parquet format.

    Takes a list of lists (each one containing tweets fields collected
    from a tweet), creates a pandas data frame, and uploads to s3 in
    parquet format. Then it loggs to the process logger (defined in the
    scope of the main module).

    It creates the key of the file using the timestamp of the moment of
    execution.

    Parameters
    ----------
        logger: Logger
            Logger object where to log the events
        bucket:str
            the S3 bucket where to upload the files
        prefix: str
            the prefix (directory path) to save the file
        tweets: list
            list of lists with tweet fields
    """
    key = f"s3://{bucket}/{prefix}" + str(datetime.now()) + ".parquet"
    tweets_df = pd.DataFrame(tweets)
    tweets_df.columns = [
        "tweet_id",
        "text",
        "created_at",
        "username",
        "location",
        "coordinates",
        "retweet_count",
        "retweeted",
        "source",
        "favorite_count",
        "favorited",
        "in_reply_to_status_id_str",
    ]

    tweets_df.to_parquet(key)

    logger.info("Saved %s  tweets in s3, filename %s", str(len(tweets_df)), key)
