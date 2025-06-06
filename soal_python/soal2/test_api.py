import unittest
import json
from soal2 import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post_Request(self, payload):
        print("\nInput:", payload)
        response = self.client.post(
            '/api/rafif',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = response.get_json()
        print("Output:", data)
        return data

    def test_Nilai_A(self):
        data = self.post_Request({"nilai": 85})
        self.assertEqual(data["nilai"], "A")
        self.assertEqual(data["status"], "lulus")

    def test_Nilai_B(self):
        data = self.post_Request({"nilai": 70})
        self.assertEqual(data["nilai"], "B")
        self.assertEqual(data["status"], "lulus")

    def test_Nilai_C(self):
        data = self.post_Request({"nilai": 55})
        self.assertEqual(data["nilai"], "C")
        self.assertEqual(data["status"], "lulus")

    def test_Nilai_D(self):
        data = self.post_Request({"nilai": 40})
        self.assertEqual(data["nilai"], "D")
        self.assertEqual(data["status"], "tidak lulus")

    def test_Nilai_E(self):
        data = self.post_Request({"nilai": 25})
        self.assertEqual(data["nilai"], "E")
        self.assertEqual(data["status"], "tidak lulus")

    def test_Nilai_Kurang_Dari_0(self):
        data = self.post_Request({"nilai": -5})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_Nilai_Lebih_Dari_100(self):
        data = self.post_Request({"nilai": 150})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_Input_Bukan_Angka(self):
        data = self.post_Request({"nilai": "abc"})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")

    def test_Key_Tidak_Ada(self):
        data = self.post_Request({})
        self.assertEqual(data["nilai"], "Invalid")
        self.assertEqual(data["status"], "tidak lulus")


if __name__ == '__main__':
    unittest.main()
