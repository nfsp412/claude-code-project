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

    def test_get_json_line_count_whitespace_only(self):
        """Test line count for whitespace-only string."""
        lines = get_json_line_count("   \n\t  ")
        self.assertEqual(lines, 0)

    def test_get_json_line_count_single_line_whitespace(self):
        """Test line count with leading/trailing whitespace."""
        json_str = '  {"name": "John"}  '
        lines = get_json_line_count(json_str)
        self.assertEqual(lines, 1)


class TestFormatJsonEdgeCases(unittest.TestCase):
    """Edge case tests for format_json function."""

    def test_format_json_empty_object(self):
        """Test formatting empty object."""
        result = format_json("{}")
        self.assertEqual(result.strip(), "{}")

    def test_format_json_empty_array(self):
        """Test formatting empty array."""
        result = format_json("[]")
        self.assertEqual(result.strip(), "[]")

    def test_format_json_null(self):
        """Test formatting null value."""
        result = format_json("null")
        self.assertEqual(result.strip(), "null")

    def test_format_json_boolean_true(self):
        """Test formatting boolean true."""
        result = format_json("true")
        self.assertEqual(result.strip(), "true")

    def test_format_json_boolean_false(self):
        """Test formatting boolean false."""
        result = format_json("false")
        self.assertEqual(result.strip(), "false")

    def test_format_json_integer(self):
        """Test formatting integer."""
        result = format_json("42")
        self.assertEqual(result.strip(), "42")

    def test_format_json_float(self):
        """Test formatting float."""
        result = format_json("3.14159")
        self.assertEqual(result.strip(), "3.14159")

    def test_format_json_negative_number(self):
        """Test formatting negative number."""
        result = format_json("-100")
        self.assertEqual(result.strip(), "-100")

    def test_format_json_scientific_notation(self):
        """Test formatting scientific notation."""
        result = format_json("1.5e10")
        # Python's json.dumps may convert 1.5e10 to 15000000000.0
        # Just verify the value is correctly parsed and formatted
        self.assertIn("15000000000", result)

    def test_format_json_unicode(self):
        """Test formatting unicode characters."""
        json_str = '{"name": "张三", "city": "北京"}'
        result = format_json(json_str)
        self.assertIn("张三", result)
        self.assertIn("北京", result)

    def test_format_json_emoji(self):
        """Test formatting emoji."""
        json_str = '{"emoji": "😀🎉"}'
        result = format_json(json_str)
        self.assertIn("😀", result)
        self.assertIn("🎉", result)

    def test_format_json_nested_arrays(self):
        """Test formatting nested arrays."""
        json_str = '[[1,2],[3,4],[5,6]]'
        result = format_json(json_str)
        self.assertIn("1", result)
        self.assertIn("6", result)

    def test_format_json_deep_nesting(self):
        """Test formatting deeply nested structure."""
        json_str = '{"a":{"b":{"c":{"d":{"e":"value"}}}}}'
        result = format_json(json_str)
        self.assertIn('"e"', result)
        self.assertIn('"value"', result)

    def test_format_json_string_with_escape(self):
        """Test formatting string with escape sequences."""
        json_str = '{"newline": "line1\\nline2", "tab": "col1\\tcol2"}'
        result = format_json(json_str)
        self.assertIn("newline", result)

    def test_format_json_empty_string_value(self):
        """Test formatting empty string value."""
        json_str = '{"empty": ""}'
        result = format_json(json_str)
        self.assertIn('"empty": ""', result)

    def test_format_json_mixed_types(self):
        """Test formatting mixed types in array."""
        json_str = '[1, "two", true, null, {"key": "value"}]'
        result = format_json(json_str)
        self.assertIn("1", result)
        self.assertIn("two", result)
        self.assertIn("true", result)
        self.assertIn("null", result)


class TestMinifyJsonEdgeCases(unittest.TestCase):
    """Edge case tests for minify_json function."""

    def test_minify_json_empty_object(self):
        """Test minifying empty object."""
        result = minify_json("{}")
        self.assertEqual(result, "{}")

    def test_minify_json_empty_array(self):
        """Test minifying empty array."""
        result = minify_json("[]")
        self.assertEqual(result, "[]")

    def test_minify_json_null(self):
        """Test minifying null."""
        result = minify_json("null")
        self.assertEqual(result, "null")

    def test_minify_json_boolean(self):
        """Test minifying boolean values."""
        self.assertEqual(minify_json("true"), "true")
        self.assertEqual(minify_json("false"), "false")

    def test_minify_json_numbers(self):
        """Test minifying numbers."""
        self.assertEqual(minify_json("42"), "42")
        self.assertEqual(minify_json("3.14"), "3.14")

    def test_minify_json_unicode(self):
        """Test minifying unicode content."""
        json_str = '{"name": "张三"}'
        result = minify_json(json_str)
        self.assertEqual(result, '{"name":"张三"}')

    def test_minify_json_already_minified(self):
        """Test minifying already minified JSON."""
        json_str = '{"a":1,"b":2}'
        result = minify_json(json_str)
        self.assertEqual(result, '{"a":1,"b":2}')

    def test_minify_json_extra_whitespace(self):
        """Test minifying JSON with extra whitespace."""
        json_str = '  {  "key" : "value"  }  '
        result = minify_json(json_str)
        self.assertEqual(result, '{"key":"value"}')


class TestValidateJsonEdgeCases(unittest.TestCase):
    """Edge case tests for validate_json function."""

    def test_validate_json_empty_string(self):
        """Test validating empty string."""
        result = validate_json("")
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])

    def test_validate_json_whitespace_only(self):
        """Test validating whitespace-only string."""
        result = validate_json("   ")
        self.assertFalse(result["valid"])

    def test_validate_json_primitives(self):
        """Test validating primitive values."""
        self.assertTrue(validate_json('"string"')["valid"])
        self.assertTrue(validate_json("123")["valid"])
        self.assertTrue(validate_json("true")["valid"])
        self.assertTrue(validate_json("false")["valid"])
        self.assertTrue(validate_json("null")["valid"])

    def test_validate_json_array_root(self):
        """Test validating array as root."""
        result = validate_json("[1, 2, 3]")
        self.assertTrue(result["valid"])

    def test_validate_json_single_quote(self):
        """Test validating single quotes (should fail)."""
        result = validate_json("{'key': 'value'}")
        self.assertFalse(result["valid"])

    def test_validate_json_trailing_comma(self):
        """Test validating trailing comma (should fail)."""
        result = validate_json('{"key": "value",}')
        self.assertFalse(result["valid"])

    def test_validate_json_unquoted_key(self):
        """Test validating unquoted key (should fail)."""
        result = validate_json('{key: "value"}')
        self.assertFalse(result["valid"])

    def test_validate_json_missing_closing(self):
        """Test validating missing closing brace."""
        result = validate_json('{"key": "value"')
        self.assertFalse(result["valid"])


class TestGetJsonSizeEdgeCases(unittest.TestCase):
    """Edge case tests for get_json_size function."""

    def test_get_json_size_empty(self):
        """Test size of empty JSON."""
        size = get_json_size("{}")
        self.assertEqual(size, 2)

    def test_get_json_size_unicode(self):
        """Test size calculation with unicode."""
        json_str = '{"name": "张三"}'
        size = get_json_size(json_str)
        self.assertEqual(size, len(json_str.encode('utf-8')))

    def test_get_json_size_emoji(self):
        """Test size calculation with emoji (4 bytes each)."""
        json_str = '{"emoji": "😀"}'
        size = get_json_size(json_str)
        self.assertEqual(size, len(json_str.encode('utf-8')))

    def test_get_json_size_large_number(self):
        """Test size with large number."""
        json_str = '{"big": 12345678901234567890}'
        size = get_json_size(json_str)
        self.assertEqual(size, len(json_str.encode('utf-8')))


class TestGetJsonLineCountEdgeCases(unittest.TestCase):
    """Additional edge case tests for get_json_line_count."""

    def test_get_json_line_count_invalid_json(self):
        """Test line count with invalid JSON."""
        with self.assertRaises(ValueError):
            get_json_line_count("{invalid}")

    def test_get_json_line_count_many_lines(self):
        """Test line count with many lines."""
        json_str = '{\n' + ',\n'.join([f'  "key{i}": "value{i}"' for i in range(100)]) + '\n}'
        lines = get_json_line_count(json_str)
        self.assertEqual(lines, 102)


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


class TestValidateColumnOrderEdgeCases(unittest.TestCase):
    """Additional edge case tests for validate_column_order."""

    def test_reader_column_type_array_of_strings(self):
        """Reader columns as array of strings with backticks."""
        js = _make_datax_json(["`col1`", "`col2`"], ["col1", "col2"])
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_reader_column_type_array_of_dicts(self):
        """Reader columns as array of dicts should raise ValueError (unsupported format)."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": [{"name": "id"}, {"name": "name"}]}},
                    "writer": {"parameter": {"column": [{"name": "id"}, {"name": "name"}]}},
                }]
            }
        })
        # Reader expects strings with backticks, dicts are not supported
        with self.assertRaises(AttributeError):
            validate_column_order(js)

    def test_writer_column_mixed_format(self):
        """Writer with mixed name-only and name/type format."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                    "writer": {"parameter": {"column": ["id", {"name": "name"}]}},
                }]
            }
        })
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_column_name_with_underscore(self):
        """Column names with underscores."""
        js = _make_datax_json(
            ["`user_id`", "`created_at`", "`updated_at`"],
            [{"name": "user_id", "type": "bigint"}, {"name": "created_at", "type": "timestamp"}, {"name": "updated_at", "type": "timestamp"}]
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_column_name_with_hyphen(self):
        """Column names with hyphens."""
        js = _make_datax_json(
            ["`user-id`", "`first-name`"],
            [{"name": "user-id", "type": "string"}, {"name": "first-name", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_column_name_case_mismatch(self):
        """Column names with case mismatch."""
        js = _make_datax_json(
            ["`ID`", "`Name`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])

    def test_duplicate_columns_in_reader(self):
        """Duplicate column names in reader."""
        js = _make_datax_json(
            ["`id`", "`id`", "`name`"],
            [{"name": "id", "type": "bigint"}, {"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_duplicate_columns_in_writer(self):
        """Duplicate column names in writer."""
        js = _make_datax_json(
            ["`id`", "`name`"],
            [{"name": "id", "type": "bigint"}, {"name": "id", "type": "bigint"}]
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        self.assertEqual(result["results"][0]["reader_count"], 2)
        self.assertEqual(result["results"][0]["writer_count"], 2)

    def test_column_with_numeric_name(self):
        """Column with numeric-only name."""
        js = _make_datax_json(
            ["`123`", "`456`"],
            [{"name": "123", "type": "string"}, {"name": "456", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_column_with_special_characters(self):
        """Column names with special characters."""
        js = _make_datax_json(
            ["`col@name`", "`col.name`", "`col:name`"],
            [{"name": "col@name", "type": "string"}, {"name": "col.name", "type": "string"}, {"name": "col:name", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_extra_fields_in_writer_column(self):
        """Writer column objects with extra fields beyond name/type."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`"]}},
                    "writer": {"parameter": {"column": [{"name": "id", "type": "bigint", "extra": "ignored"}]}},
                }]
            }
        })
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_writer_column_missing_name_field(self):
        """Writer column object missing name field should raise ValueError."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`"]}},
                    "writer": {"parameter": {"column": [{"type": "bigint"}]}},
                }]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("invalid format", str(ctx.exception))

    def test_reader_parameter_missing(self):
        """Reader missing parameter field."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"other": {}},
                    "writer": {"parameter": {"column": []}},
                }]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("reader.parameter.column", str(ctx.exception))

    def test_writer_parameter_missing(self):
        """Writer missing parameter field."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": []}},
                    "writer": {"other": {}},
                }]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("writer.parameter.column", str(ctx.exception))

    def test_reader_column_not_array(self):
        """Reader column not being an array."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": "`id`"}},
                    "writer": {"parameter": {"column": []}},
                }]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("reader.parameter.column must be an array", str(ctx.exception))

    def test_writer_column_not_array(self):
        """Writer column not being an array."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": []}},
                    "writer": {"parameter": {"column": "id"}},
                }]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        self.assertIn("writer.parameter.column must be an array", str(ctx.exception))

    def test_content_item_not_dict(self):
        """Content item not being a dict."""
        js = json.dumps({
            "job": {
                "content": [["not", "a", "dict"]]
            }
        })
        with self.assertRaises(ValueError) as ctx:
            validate_column_order(js)
        # Should fail when trying to access reader key
        self.assertIn("reader", str(ctx.exception))

    def test_large_number_of_columns(self):
        """Test with large number of columns."""
        reader_cols = [f"`col{i}`" for i in range(100)]
        writer_cols = [{"name": f"col{i}", "type": "string"} for i in range(100)]
        js = _make_datax_json(reader_cols, writer_cols)
        result = validate_column_order(js)
        self.assertTrue(result["valid"])
        self.assertEqual(result["results"][0]["reader_count"], 100)
        self.assertEqual(result["results"][0]["writer_count"], 100)

    def test_partial_match_then_mismatch(self):
        """First columns match, later ones don't."""
        js = _make_datax_json(
            ["`a`", "`b`", "`c`", "`d`"],
            [{"name": "a", "type": "string"}, {"name": "b", "type": "string"}, {"name": "x", "type": "string"}, {"name": "y", "type": "string"}]
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        mismatches = result["results"][0]["mismatches"]
        self.assertEqual(len(mismatches), 2)
        self.assertEqual(mismatches[0]["position"], 3)
        self.assertEqual(mismatches[1]["position"], 4)


if __name__ == "__main__":
    unittest.main()
