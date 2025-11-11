#!/usr/bin/env python3
"""Unit tests for the utils module."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    #Tests for the utils.access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: dict, path: tuple, expected
    ) -> None:
        #Verify that access_nested_map returns the expected value."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self, nested_map: dict, path: tuple
    ) -> None:
        #Ensure that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    #Tests for the utils.get_json function.

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        #Confirm that get_json returns the expected JSON response.
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value.json.return_value = test_payload
            self.assertEqual(utils.get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
        #Tests for the utils.memoize decorator.

    def test_memoize(self) -> None:
        #Verify that memoize caches the result after the first method call."""
        class TestClass:
        #Helper class to test the memoization behavior

            def a_method(self) -> int:
                #Return a fixed integer value.
                return 42

            @utils.memoize
            def a_property(self) -> int:
                #Return the value of a_method using memoization
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mocked.assert_called_once()
