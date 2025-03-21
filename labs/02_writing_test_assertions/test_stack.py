from unittest import TestCase
from stack import Stack

class TestStack(TestCase):
    """Test cases for Stack"""

    def setUp(self):
        """Setup before each test"""
        self.stack = Stack()

    def tearDown(self):
        """Tear down after each test"""
        self.stack = None

    def test_push(self):
        """Test pushing an item into the stack"""
        self.stack.push(5)
        self.assertEqual(self.stack.peek(), 5)
        self.assertEqual(self.stack.pop(), 5)

        self.stack.push(5)
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.peek(), 5)
        self.assertEqual(self.stack.pop(), 5)

        self.assertRaises(IndexError, lambda: self.stack.pop())

    def test_pop(self):
        """Test popping an item of off the stack"""
        self.stack.push(5)
        self.assertEqual(self.stack.peek(), 5)
        self.assertEqual(self.stack.pop(), 5)

        self.stack.push(5)
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.peek(), 5)
        self.assertEqual(self.stack.pop(), 5)

        self.assertRaises(IndexError, lambda: self.stack.pop())

    def test_peek(self):
        """Test peeking at the top the stack"""
        self.assertRaises(IndexError, lambda: self.stack.peek())

        self.stack.push(5)
        self.stack.push(3)
        self.assertEqual(self.stack.peek(), 3)

        self.stack.pop()
        self.assertEqual(self.stack.peek(), 5)

        self.stack.pop()
        self.assertRaises(IndexError, lambda: self.stack.peek())

    def test_is_empty(self):
        """Test if the stack is empty"""
        self.assertTrue(self.stack.is_empty())

        self.stack.push(5)
        self.assertFalse(self.stack.is_empty())

        self.stack.pop()
        self.assertTrue(self.stack.is_empty())
