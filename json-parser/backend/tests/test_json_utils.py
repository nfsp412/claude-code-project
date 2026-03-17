"""Unit tests for JSON utility functions."""

import unittest

from app.utils.json_utils import (
    format_json,
    minify_json,
    validate_json,
    get_json_size,
    get_json_line_count,
)


class TestFormatJson(unittest.TestCase):
    """Tests for format_json function."""

    def test_format_json_valid(self):
        """Test formatting a valid JSON string."""
        json_str = '{"name":"John","age":30}'
        result = format_json(json_str)
        self.assertIn('"name": "John"', result)
        self.assertIn('"age": 30', result)

    def test_format_json_custom_indent(self):
        """Test formatting with custom indent value."""
        json_str = '{"name":"John","age":30}'
        result = format_json(json_str, indent=4)
        # Check that 4-space indentation is used
        self.assertIn('    "name"', result)

    def test_format_json_invalid(self):
        """Test that invalid JSON raises ValueError."""
        json_str = '{"name": "John",}'
        with self.assertRaises(ValueError):
            format_json(json_str)


class TestMinifyJson(unittest.TestCase):
    """Tests for minify_json function."""

    def test_minify_json_valid(self):
        """Test minifying a valid JSON string."""
        json_str = '{\n  "name": "John",\n  "age": 30\n}'
        result = minify_json(json_str)
        self.assertEqual(result, '{"name":"John","age":30}')

    def test_minify_json_with_whitespace(self):
        """Test minifying JSON with extra whitespace."""
        json_str = '  {  "name" :  "John"  }  '
        result = minify_json(json_str)
        self.assertEqual(result, '{"name":"John"}')


class TestValidateJson(unittest.TestCase):
    """Tests for validate_json function."""

    def test_validate_json_valid(self):
        """Test validating a valid JSON string."""
        json_str = '{"name": "John", "age": 30}'
        result = validate_json(json_str)
        self.assertTrue(result["valid"])
        self.assertIsNone(result["error"])

    def test_validate_json_invalid(self):
        """Test validating an invalid JSON string."""
        json_str = '{"name": "John",}'
        result = validate_json(json_str)
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])


class TestGetJsonSize(unittest.TestCase):
    """Tests for get_json_size function."""

    def test_get_json_size(self):
        """Test calculating JSON size in bytes."""
        json_str = '{"name": "John"}'
        size = get_json_size(json_str)
        self.assertEqual(size, len(json_str.encode('utf-8')))


class TestGetJsonLineCount(unittest.TestCase):
    """Tests for get_json_line_count function."""

    def test_get_json_line_count_single(self):
        """Test line count for single-line JSON."""
        json_str = '{"name": "John", "age": 30}'
        lines = get_json_line_count(json_str)
        self.assertEqual(lines, 1)

    def test_get_json_line_count_multi(self):
        """Test line count for multi-line JSON."""
        json_str = '{\n  "name": "John",\n  "age": 30\n}'
        lines = get_json_line_count(json_str)
        self.assertEqual(lines, 4)

    def test_get_json_line_count_empty(self):
        """Test line count for empty string."""
        lines = get_json_line_count("")
        self.assertEqual(lines, 0)


if __name__ == "__main__":
    unittest.main()
