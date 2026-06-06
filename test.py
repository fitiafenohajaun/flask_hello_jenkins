import unittest
import app


class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()

    def test_root(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.data, b"Hello World!\n")

    def test_hello(self):
        rv = self.client.get("/hello/")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.data, b"Hello World!\n")

    def test_hello_name(self):
        rv = self.client.get("/hello/Simon")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b"Simon", rv.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)