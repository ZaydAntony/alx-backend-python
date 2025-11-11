#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: dict, path: tuple, expected
    ) -> None:
        
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self, nested_map: dict, path: tuple
    ) -> None:
        
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value.json.return_value = test_payload
            self.assertEqual(utils.get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    

    def test_memoize(self) -> None:
        
        class TestClass:
            def a_method(self) -> int:
                return 42

            @utils.memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mocked.assert_called_once()
