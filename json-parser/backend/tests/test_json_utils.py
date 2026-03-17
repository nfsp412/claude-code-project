"""Unit tests for JSON utility functions."""

import json
import unittest

from app.utils.json_utils import (
    format_json,
    minify_json,
    validate_json,
    get_json_size,
    get_json_line_count,
    validate_column_order,
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

    def test_format_json_with_tab_indent(self):
        """Test formatting JSON with tab indentation."""
        json_str = '{"name":"John","age":30}'
        result = format_json(json_str, indent="tab")
        # 制表符缩进应该使用 \t 而不是空格
        self.assertIn("\t\"name\"", result)
        self.assertTrue(result.startswith("{\n\t"))

    def test_format_json_with_tab_indent_nested(self):
        """Test formatting nested JSON with tab indentation."""
        json_str = '{"user":{"name":"John","address":{"city":"NYC"}}}'
        result = format_json(json_str, indent="tab")
        # 检查嵌套结构使用制表符
        self.assertIn("\t\"user\"", result)
        self.assertIn("\t\t\"name\"", result)
        self.assertIn("\t\t\t\"city\"", result)

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


def _make_datax_json(reader_cols, writer_cols):
    """Helper to build a minimal DataX config JSON string."""
    return json.dumps({
        "job": {
            "content": [{
                "reader": {"parameter": {"column": reader_cols}},
                "writer": {"parameter": {"column": writer_cols}},
            }]
        }
    })


class TestValidateColumnOrder(unittest.TestCase):
    """Tests for validate_column_order function."""

    def test_matching_columns(self):
        """Columns in same order should pass validation."""
        js = _make_datax_json(
            ["`id`", "`name`", "`age`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}, {"name": "age", "type": "int"}],
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["mismatches"], [])

    def test_mismatched_order(self):
        """Swapped columns should report mismatches at correct positions."""
        js = _make_datax_json(
            ["`id`", "`age`", "`name`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}, {"name": "age", "type": "int"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        mismatches = result["results"][0]["mismatches"]
        self.assertEqual(len(mismatches), 2)
        self.assertEqual(mismatches[0]["position"], 2)
        self.assertEqual(mismatches[0]["reader_field"], "age")
        self.assertEqual(mismatches[0]["writer_field"], "name")
        self.assertEqual(mismatches[1]["position"], 3)
        self.assertEqual(mismatches[1]["reader_field"], "name")
        self.assertEqual(mismatches[1]["writer_field"], "age")

    def test_reader_has_more_columns(self):
        """Extra reader columns should appear as mismatches with None writer_field."""
        js = _make_datax_json(
            ["`id`", "`name`", "`extra`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        r = result["results"][0]
        self.assertEqual(r["reader_count"], 3)
        self.assertEqual(r["writer_count"], 2)
        self.assertEqual(len(r["mismatches"]), 1)
        self.assertEqual(r["mismatches"][0]["position"], 3)
        self.assertEqual(r["mismatches"][0]["reader_field"], "extra")
        self.assertIsNone(r["mismatches"][0]["writer_field"])

    def test_writer_has_more_columns(self):
        """Extra writer columns should appear as mismatches with None reader_field."""
        js = _make_datax_json(
            ["`id`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        r = result["results"][0]
        self.assertEqual(r["reader_count"], 1)
        self.assertEqual(r["writer_count"], 2)
        self.assertEqual(r["mismatches"][0]["position"], 2)
        self.assertIsNone(r["mismatches"][0]["reader_field"])
        self.assertEqual(r["mismatches"][0]["writer_field"], "name")

    def test_empty_columns(self):
        """Both empty column arrays should pass validation."""
        js = _make_datax_json([], [])
        result = validate_column_order(js)
        self.assertTrue(result["valid"])
        self.assertEqual(result["results"][0]["reader_count"], 0)
        self.assertEqual(result["results"][0]["writer_count"], 0)

    def test_invalid_json(self):
        """Invalid JSON string should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            validate_column_order("{bad json")
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_missing_job_field(self):
        """Missing 'job' field should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"not_job": {}}')
        self.assertIn("job", str(ctx.exception))

    def test_missing_content_field(self):
        """Missing 'job.content' should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"job": {}}')
        self.assertIn("content", str(ctx.exception))

    def test_empty_content_array(self):
        """Empty 'job.content' array should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"job": {"content": []}}')
        self.assertIn("content", str(ctx.exception))

    def test_missing_reader_column(self):
        """Missing reader.parameter.column should raise ValueError."""
        js = json.dumps({
            "job": {"content": [{"reader": {"parameter": {}}, "writer": {"parameter": {"column": []}}}]}
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("reader.parameter.column", str(ctx.exception))

    def test_missing_writer_column(self):
        """Missing writer.parameter.column should raise ValueError."""
        js = json.dumps({
            "job": {"content": [{"reader": {"parameter": {"column": []}}, "writer": {"parameter": {}}}]}
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("writer.parameter.column", str(ctx.exception))

    def test_multiple_content_items(self):
        """Should validate each content item independently."""
        js = json.dumps({
            "job": {
                "content": [
                    {
                        "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                        "writer": {"parameter": {"column": [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}]}},
                    },
                    {
                        "reader": {"parameter": {"column": ["`a`", "`b`"]}},
                        "writer": {"parameter": {"column": [{"name": "b", "type": "string"}, {"name": "a", "type": "string"}]}},
                    },
                ]
            }
        })
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["results"]), 2)
        self.assertTrue(result["results"][0]["valid"])
        self.assertFalse(result["results"][1]["valid"])
        self.assertEqual(len(result["results"][1]["mismatches"]), 2)

    def test_writer_string_columns(self):
        """Writer columns as plain strings (no name/type objects) should also work."""
        js = _make_datax_json(
            ["`id`", "`name`"],
            ["id", "name"],
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_json_root_not_object(self):
        """JSON root being an array should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            validate_column_order("[1, 2, 3]")
        self.assertIn("object", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
