import unittest
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_h1_present(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("## No main title here")

if __name__ == "__main__":
    unittest.main()
