"""
This module contains a dummy secret management class and associated exception.
"""

import os

class SecretException(Exception):
    """
    Simple exception class to signal errors related to secrets management.
    """
    def __init__(self, message):
        super().__init__(message)


class Secret:
    """
This class implements a fake secret store and is used to retrieve the bearer key necessary to authenticate with twitter.
    """
    def get_secret(self, key):
        """
        Return the value for the key given in argument. Note that as this is a fake store, the only legal key is "BEARER", and its value must come from the file `cwd`/bearer.txt.

        Arguments
        ----------
        key: str
            The key for the value we want to retrieve
        """
        if key != 'BEARER':
            raise SecretException("No such key:" + key)
        else:
            with open(os.getcwd() + "/bearer.txt") as f:
                return f.read().strip()

