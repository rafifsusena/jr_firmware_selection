import unittest
import json
from soal2 import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_nilai_valid(self):
        response = self.client.post('/api/rafif',
                                    data=json.dumps({"nilai": 85}),
                                    content_type='application/json')
        data = response.get_json()
        self.assertEqual(data["nilai"], "A")
        self.assertEqual(data["status"], "lulus")

    def test_nilai_tidak_valid(self):
        response = self.client.post('/api/rafif',
                                    data=json.dumps({"nilai": -10}),
                                    content_type='application/json')
        data = response.get_json()
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_key_tidak_ada(self):
        response = self.client.post('/api/rafif',
                                    data=json.dumps({}),
                                    content_type='application/json')
        data = response.get_json()
        self.assertEqual(data["nilai"], "Invalid")

if __name__ == '__main__':
    unittest.main()
