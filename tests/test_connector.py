import unittest
from tweeterstream.connectors.connector import Connector

class TestConnectorCreation(unittest.TestCase):

    def test_creation_ok(self):
        class MyConnector(Connector):
            def _receive(self, tweet):
                pass

        c = MyConnector("Connector name")
        self.assertIsNotNone(c)

        


if __name__ == '__main__':
    unittest.main()
