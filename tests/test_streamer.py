import unittest
from tweeterstream import streamer
from tweeterstream.connectors.connector import Connector
from tweeterstream.secret import Secret

class TestStreamer(unittest.TestCase):

    DEFAULT_CONFIG = {
        'publish': {
            'endpoint': 'http://127.0.0.1:5000/tweets',
        },
    }

    def test_streamer_creation_ok(self):
        
        s = streamer.create_streamer(self.DEFAULT_CONFIG, Secret())
        self.assertIsNotNone(s)

    def test_add_subscribers_ok(self):
        s = streamer.create_streamer(self.DEFAULT_CONFIG, Secret())
        s = streamer.add_all_subscribers(s, {'publish': {'endpoint': 'abc'}})

        self.assertIsNotNone(s)
        self.assertEqual(1, len(s.subscribers))
        self.assertIsInstance(s.subscribers[0], Connector)


if __name__ == '__main__':
    unittest.main()
