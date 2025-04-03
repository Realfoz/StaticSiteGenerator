import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_basic_title(self):
        markdown = "# Hello World\nThis is some content."
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_with_extra_spaces(self):
        markdown = "#    Spaced Title    \nMore content."
        self.assertEqual(extract_title(markdown), "Spaced Title")
    
    def test_no_title_raises_exception(self):
        markdown = "This is content without an H1 header."
        # Test that an exception is raised
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()