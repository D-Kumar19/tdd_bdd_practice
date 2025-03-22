"""
Test Cases for Counter Web Service
"""
import status
from counter import app
from unittest import TestCase

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        data = result.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_increment_count(self):
        """It should increment the counter"""
        result = self.client.post("/counters/baz")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        base = data["baz"]

        result = self.client.put("/counters/baz")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.get_json()
        self.assertEqual(data["baz"], base + 1)

    def test_read_counter(self):
        """It should read the counter"""
        result = self.client.post("/counters/qux")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.get("/counters/qux")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.get_json()
        self.assertEqual(data["qux"], 0)

    def test_delete_counter(self):
        """It should delete the counter"""
        result = self.client.post("/counters/quux")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.delete("/counters/quux")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
