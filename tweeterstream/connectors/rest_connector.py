"""
This module provides the necessary to connect the streamer to a REST endpoint.

The class RESTConnector implements the Connector class and is responsible for POSTing the tweets received to a REST endpoint passed in its constructor.

"""
from tweeterstream.connectors.connector import Connector
import logging.config
import requests
import json

class RESTConnector(Connector):
    """
    RESTConnector is an implementation of Connector.

    """
    def __init__(self, name, endpoint):
        """
        Constructor.

        Arguments
        ---------
        name: str
            The name of this connector. *Mandatory*.
        endpoint: str
            The REST endpoint where the tweets will be POSTed to. *Mandatory*.
        """
        super().__init__(name)
        self.endpoint = endpoint
        logging.debug(f'Configured logging for RESTConnector {self.name}')
        

    def _receive(self, tweet):
        """
        This methods is responsible for POSTing the tweets to the endpoint configured in the instance.
        The content of the tweet is extracted from the tweepy.tweet instance from the member tweepy.tweet.data, and converted to JSON before being POSTed to the endpoint.
        
        Arguments
        ---------
        tweet: tweepy.Tweet
            The tweet to post to the endpoint. *Mandatory*.
        """
        logging.debug("RESTConnector about to send: ")
        logging.debug(json.dumps(tweet.data))
        requests.post(self.endpoint, json=json.dumps(tweet.data))
