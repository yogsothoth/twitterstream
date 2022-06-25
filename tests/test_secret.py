import unittest
from tweeterstream.secret import SecretException, Secret

class TestSecretRetrieval(unittest.TestCase):

    def test_retrieval_ok(self):
        s = Secret()
        value = s.get_secret("BEARER")
        self.assertIsNotNone(value)

    @unittest.expectedFailure
    def test_retrieval_failure(self):
        s = Secret()
        value = s.get_secret("MISSING")
        self.assertIsNotNone(value)

if __name__ == '__main__':
    unittest.main()
