import unittest
from ghostshell.utils import is_private_ip, extract_ip, extract_port

class TestUtils(unittest.TestCase):

    def test_is_private_ip(self):
        self.assertTrue(is_private_ip("192.168.0.1"))
        self.assertTrue(is_private_ip("10.0.0.5"))
        self.assertTrue(is_private_ip("172.16.0.1"))
        self.assertFalse(is_private_ip("8.8.8.8"))

    def test_extract_ip(self):
        self.assertEqual(extract_ip("192.168.1.1:443"), "192.168.1.1")
        self.assertEqual(extract_ip("[2001:db8::1]:80"), "2001:db8::1")

    def test_extract_port(self):
        self.assertEqual(extract_port("192.168.1.1:443"), 443)
        self.assertEqual(extract_port("[2001:db8::1]:80"), 80)
        self.assertIsNone(extract_port("noport"))

if __name__ == '__main__':
    unittest.main()
