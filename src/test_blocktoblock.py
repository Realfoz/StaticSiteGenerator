import unittest
from enum import Enum
from node_types import BlockType
from split_delimiter import block_to_block_type

class TestBlockTypeFunction(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
    
    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.heading)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.heading)
        
        # This is not a valid heading (no space after #)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.paragraph)
    
    def test_code(self):
        code_block = "```\ndef hello_world():\n    print('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.code)
        
        # Not a valid code block (missing closing backticks)
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.paragraph)
    
    def test_quote(self):
        quote_block = ">This is a quote\n>It spans multiple lines"
        self.assertEqual(block_to_block_type(quote_block), BlockType.quote)
        
        # Not a valid quote (second line doesn't start with >)
        self.assertEqual(block_to_block_type(">This is a quote\nThis is not"), BlockType.paragraph)
    
    def test_unordered_list(self):
        list_block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(list_block), BlockType.unordered_list)
                         