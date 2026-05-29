#!/usr/bin/env python3
import unittest
import app
class TestHello(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        
        
    def test_hello(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'Hello World!\n')
        
        
    def test_hello_hello(self):
        rv = self.app.get('/hello/')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'Hello World!\n')
        
        
    def test_hello_name(self):
        name = 'Simon'
        rv = self.app.get(f'/hello/{name}')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(bytearray(f"{name}", 'utf-8'), rv.data)
        
    
    def test_api_status(self):
        rv = self.app.get('/api/status')
        self.assertEqual(rv.status, '200 OK')
        
        json_data = rv.get_json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(json_data['version'], '1.0.0')
        self.assertIn("L'API fonctionne", json_data['message'])
        
        
if __name__ == '__main__':
    unittest.main()
