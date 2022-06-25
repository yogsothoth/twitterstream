import unittest
from tweeterstream.connectors.rest_connector import RESTConnector

class TestConnectorCreation(unittest.TestCase):

    def test_creation_ok(self):
        c = RESTConnector("Connector name", "http://localhost:5000")
        self.assertIsNotNone(c)


if __name__ == '__main__':
    unittest.main()
