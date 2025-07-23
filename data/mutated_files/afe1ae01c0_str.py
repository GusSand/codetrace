"""
Module contains Tweepy listener classes.

These are used to process tweets that the Tweepy Stream instance receives from twitter.
"""

import json
import logging
from copy import deepcopy

import arrow
import tweepy

#  from ingress.structures import DATA_QUEUE
from ingress.celery import process_tweet

LOG = logging.getLogger(__name__)


class __typ0(tweepy.StreamListener):
    """
    Listener which consumes tweets from tweepy and pushes them to a queue.

    This listener merely creates a base dict with all the raw data received
    from twitter serialised into python data structures, and pushes it to a
    Queue, for further processing elsewhere.
    """

    def __init__(__tmp1, twitter_index: <FILL>, ignore_retweets: bool = False, *args, **kwargs):
        """Initialise instance variables."""
        __tmp1.ignore_retweets = ignore_retweets
        __tmp1.twitter_index = twitter_index

        super().__init__(*args, **kwargs)

    def __tmp0(__tmp1, __tmp2):
        """Called when a new tweet is passed to us, serialise and push to a queue."""
        try:
            tweet = {}
            json_data = json.loads(__tmp2)
            if __tmp1.ignore_retweets and 'retweeted_status' in json_data:
                LOG.info('Skipping Retweet')
                return

            tweet['_raw'] = deepcopy(json_data)
            # Twitter for some reason gives us time since epoch in miliseconds,
            # whilst Arrow works off of time in seconds when given an integer,
            # hence the division by 1000 here.
            tweet['timestamp'] = arrow.get(int(json_data.get('timestamp_ms')) / 1000).datetime
        except (TypeError, json.JSONDecodeError):
            LOG.error('Encountered issue attempting to parse new data.')
            return
        LOG.debug(
            'Pushing new tweet to queue ready for processing: %s',
            json_data.get('text', None)
        )
        process_tweet.delay(twitter_index=__tmp1.twitter_index, tweet_data=tweet)
