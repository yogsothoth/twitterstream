"""
This module defines a class to stream tweets from twitter.

Implementation and rationale
----------------------------
The module defines a single class, TweetStreamer, that derives from tweepy.StreamingClient. It follows a pub/sub pattern for broadcasting the tweets received.

Subscribers are expected to derived from tweeterstream.connector.Connector. Error management at their level is provided by the subscribed connectors, as their design captures prevents any exception from escaping them.

Examples
--------
.. code-block:: python

  streamer = tweeterstream.TweetStreamer("BEARER KEY")
  streamer.apply_rule("#coop")
  streamer.filter() # puts the server in a loop

Limitations
-----------
As this is a simple implementation, publishing is done in a synchronous manner.
"""
import tweepy
from flask import jsonify
import logging.config

class TweetStreamer(tweepy.StreamingClient):

    def __init__(self, key):
        """
        Constructor.

        Arguments
        ---------
        key: str
            The bearer key to authenticate with Twitter.
        """
        super().__init__(key)
        self.subscribers = []
        
    def apply_rule(self, rule):
        """
        Apply the given rule, typically a hashtag.

        Arguments
        ----------
        rule: str
            The rule to apply, in the form of a hashtag (e.g. '#coop')

        """
        self.add_rules(tweepy.StreamRule(rule))
        
    def on_tweet(self, tweet):
        """
        Callback method called upon the arrival of a new tweet: publishes to subscribers.

        Arguments
        ---------
        tweet: tweepy.Tweet
            The new tweet to despatch

        """
        logging.debug("The streamer has received a new tweet")
        return self.publish(tweet)

    def publish(self, tweet):
        """
        Publish a new tweet to all subscribers registered. Subscribers are expected to offer a method ``receive(tweet)``.

        Arguments
        ---------
        tweet: tweepy.Tweet
            The tweet to publish to subscribers.
        """
        logging.debug("Publishing a new tweet")
        for subscriber in self.subscribers:
            subscriber.receive(tweet)

    def add_subscriber(self, subscriber):
        """
        Add a subscriber to the list of subscribers. See ``publish`` in this class.

        Arguments
        ---------
        subscriber: tweeterstream.connectors.Connector
            The subscriber to add. Strictly speaking, an instance of any class would do, provided a method ``receive(tweet)`` is available, but to keep a uniform interface for all connectors, a instance of a class derived from Connector is prefered.
        """
        self.subscribers.append(subscriber)
        logging.debug(f'Added subscriber {subscriber.name}')
