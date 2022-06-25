"""
**streamer** starts a server streaming tweets from twitter and publishing them to a number of subscribers.

This script configures a default logging subsystem with a root logger to the console.

Examples
--------
.. code-block:: sh

  $ python -m tweeterstream.streamer --help
  $ python -m tweeterstream.streamer --tag nature


Attributes
----------
streamer : tweetstreamer.TweetStreamer
    The tweet streamer instance.
rest: tweetstreamer.connectors.RESTConnector
    A REST connector.
DEFAULT_LOGGING: dict
    A python dictionary holding the configuration of the logging subsystem.

"""
from tweeterstream.tweetstreamer import TweetStreamer
import typer
import logging.config
import configparser
from tweeterstream.connectors.rest_connector import RESTConnector
from tweeterstream.secret import Secret

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': 'DEBUG',
        },
        'another.module': {
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)

DEFAULT_CONFIG = {
    'publish': {
        'endpoint': 'http://127.0.0.1:5000/tweets',
    },
}

def create_streamer(config, secret):
    """
    Create the streamer instance and pass it the bearer key retrieved from the secret store.
    
    Arguments
    ---------
    config: dict
        The configuration dictionary
    secret: tweeterstream.secret.Secret
        The secret store from which the bearer key can be retrieved
    """
    streamer = TweetStreamer(secret.get_secret("BEARER"))
    return streamer
    
def add_all_subscribers(streamer, config):
    """
    Add all subscribers to the streamer instance. A real-life one would retrieve them from a configuation file and do some sanity check and validation.

    Arguments
    ---------
    streamer: tweeterstream.tweetstreamer.TweetStreamer
        The streamer instance
    config: dict
        The configuration dictionary
    """
    rest = RESTConnector("REST Connector", config['publish']['endpoint'])
    streamer.add_subscriber(rest)
    
    return streamer
        
def read_configuration(config_file, default_config):
    """
    Read the configuration file and merge it with the default configuation values.

    Arguments
    ---------
    config_file: str
        The path, including the filename, to the configuration file

    default_config: dict
        A dictionary containing the default configuration values
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    config_dict = {s:dict(config.items(s)) for s in config.sections()}
    default_config.update(config_dict)
    return default_config


def main(configfile: str = typer.Option("conf/streamer.ini", help="The configuration file"),
         tag: str = typer.Option("nature", help="A hashtag to stream, without the leading #")):
    """
    Start the streaming server, applying a rule for the tag provided on the command line and the configuration values found in the configuration file.
    """
    logging.debug("Reading the configuration")
    
    config = read_configuration(configfile, DEFAULT_CONFIG)
    
    logging.info("Starting the streamer")
    
    logging.debug("Creating the streamer")
    secret = Secret()
    streamer = create_streamer(config, secret)
    
    logging.debug("Adding all subscribers")
    streamer = add_all_subscribers(streamer, config)
    
    logging.debug("Applying the rules")
    streamer.apply_rule(f'#{tag}')

    logging.debug("Applying the filter and running the server")
    streamer.filter()

if __name__ == '__main__':
    typer.run(main)
