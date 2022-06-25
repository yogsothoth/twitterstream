"""
This module offers a common base for all connectors. 

Implementation and rationale
----------------------------
This base class follows the Non-Virtual Interface pattern: derived classes must implement the private method _receive, and users of connectors call the non-virtual method receive, which is implemented in this class. This allows to control the behaviour of all derived classes from a single location, and present a uniform interface to users.


Example
-------
.. code-block:: python
   
 from tweetstreamer.connectors.connector import Connector
 
 class MyConnector(Connector):
   def _receive(self, tweet):
     print(tweet)

"""
from abc import ABC, abstractmethod
import logging

class Connector(ABC):
    """
    Abstract Base Class for all connectors.
    """
    def __init__(self, name):
        """
        Constructor.
        
        Arguments
        ---------
        name: str
            The name of the connector. *Mandatory*.
        """
        self.name = name
    
    def receive(self, tweet):
        """
        Accept and act on a tweet. 
        The actual processing is expected to be defined in the method _receive, which is called from this method. The call is surrounded by a try/except block designed to not propagate the exceptions further. Specialised exceptions should be handled in the implementation of the _receive method, and general exceptions will be captured here. This allows for a self-contained class.
        """
        logging.debug("Received a tweet")
        try:
            self._receive(tweet)
        except Exception as e:
            logging.info("Exception while receiving a tweet:", e)
        

    @abstractmethod
    def _receive(self, tweet):
        """
        This method must be implemented by derived classes, and should handle the processing of the tweet. Called by receive.

        Arguments
        --------
        tweet: tweepy.Tweet
            The tweet to process.
        """
        ...
    
