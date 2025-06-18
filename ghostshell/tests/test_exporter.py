import unittest
import tempfile
import os
from ghostshell.exporter import export_to_json, export_to_csv

sample_data = [
    {
        "time": "now", "proto": "TCP", "local": "127.0.0.1:1234", "remote": "8.8.8.8:443",
        "status": "LISTEN", "pid": "123", "country": "US", "isp": "Google",
        "suspicious": False, "reason": ""
    }
]

class TestExporter(unittest.TestCase):

    def test_export_to_json(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
            temp_path = tf.name
        export_to_json(sample_data, temp_path)
        self.assertTrue(os.path.getsize(temp_path) > 0)
        os.unlink(temp_path)

    def test_export_to_csv(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tf:
            temp_path = tf.name
        export_to_csv(sample_data, temp_path)
        self.assertTrue(os.path.getsize(temp_path) > 0)
        os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
