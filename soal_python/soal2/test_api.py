import unittest
import json
from soal2 import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post_request(self, payload):
        print("\nInput:", payload)
        response = self.client.post(
            '/api/rafif',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = response.get_json()
        print("Output:", data)
        return data

    def test_nilai_A(self):
        data = self.post_request({"nilai": 85})
        self.assertEqual(data["nilai"], "A")
        self.assertEqual(data["status"], "lulus")

    def test_nilai_B(self):
        data = self.post_request({"nilai": 70})
        self.assertEqual(data["nilai"], "B")
        self.assertEqual(data["status"], "lulus")

    def test_nilai_C(self):
        data = self.post_request({"nilai": 55})
        self.assertEqual(data["nilai"], "C")
        self.assertEqual(data["status"], "lulus")

    def test_nilai_D(self):
        data = self.post_request({"nilai": 40})
        self.assertEqual(data["nilai"], "D")
        self.assertEqual(data["status"], "tidak lulus")

    def test_nilai_E(self):
        data = self.post_request({"nilai": 25})
        self.assertEqual(data["nilai"], "E")
        self.assertEqual(data["status"], "tidak lulus")

    def test_nilai_kurang_dari_0(self):
        data = self.post_request({"nilai": -5})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_nilai_lebih_dari_100(self):
        data = self.post_request({"nilai": 150})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_input_bukan_angka(self):
        data = self.post_request({"nilai": "abc"})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_key_tidak_ada(self):
        data = self.post_request({})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")


if __name__ == '__main__':
    unittest.main()
