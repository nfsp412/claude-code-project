"""Unit tests for json_utils module."""

import json
import unittest

from app.utils.json_utils import (
    format_json,
    minify_json,
    validate_json,
    get_json_size,
    get_json_line_count,
    validate_column_order,
    _extract_content,
    _extract_reader_columns,
    _extract_writer_columns,
)


class TestFormatJson(unittest.TestCase):
    """Tests for format_json function."""

    def test_default_indent_2(self):
        result = format_json('{"name":"John","age":30}')
        self.assertIn('"name": "John"', result)
        self.assertIn('"age": 30', result)
        self.assertIn('\n  ', result)

    def test_indent_4(self):
        result = format_json('{"a":1}', indent=4)
        self.assertIn('\n    "a"', result)

    def test_indent_8(self):
        result = format_json('{"a":1}', indent=8)
        self.assertIn('\n        "a"', result)

    def test_tab_indent(self):
        result = format_json('{"a":1}', indent="tab")
        self.assertIn('\t"a"', result)

    def test_invalid_json_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            format_json('{"name": "John",}')
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_primitive_null(self):
        result = format_json("null")
        self.assertEqual(result.strip(), "null")

    def test_primitive_number(self):
        result = format_json("42")
        self.assertEqual(result.strip(), "42")

    def test_primitive_string(self):
        result = format_json('"hello"')
        self.assertEqual(result.strip(), '"hello"')

    def test_primitive_boolean(self):
        result = format_json("true")
        self.assertEqual(result.strip(), "true")

    def test_empty_object(self):
        result = format_json("{}")
        self.assertEqual(result.strip(), "{}")

    def test_empty_array(self):
        result = format_json("[]")
        self.assertEqual(result.strip(), "[]")

    def test_unicode_preserved(self):
        result = format_json('{"name":"张三"}')
        self.assertIn("张三", result)

    def test_nested_json(self):
        result = format_json('{"a":{"b":{"c":1}}}')
        self.assertIn('"a"', result)
        self.assertIn('"b"', result)
        self.assertIn('"c"', result)

    def test_array_root(self):
        result = format_json('[{"id":1},{"id":2}]')
        self.assertIn('"id": 1', result)
        self.assertIn('"id": 2', result)

    def test_boolean_values(self):
        result = format_json('{"active":true,"disabled":false}')
        self.assertIn('"active": true', result)
        self.assertIn('"disabled": false', result)

    def test_number_types(self):
        result = format_json('{"int":42,"float":3.14,"negative":-10,"exp":1.5e10}')
        self.assertIn('"int": 42', result)
        self.assertIn('"float": 3.14', result)
        self.assertIn('"negative": -10', result)

    def test_special_characters(self):
        result = format_json('{"key":"value with\\nnewline","tab":"with\\ttab"}')
        self.assertIn("value with\\nnewline", result)


class TestMinifyJson(unittest.TestCase):
    """Tests for minify_json function."""

    def test_removes_whitespace(self):
        result = minify_json('{\n  "name": "John",\n  "age": 30\n}')
        self.assertEqual(result, '{"name":"John","age":30}')

    def test_already_compact(self):
        result = minify_json('{"a":1}')
        self.assertEqual(result, '{"a":1}')

    def test_invalid_json_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            minify_json("{bad}")
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_unicode_preserved(self):
        result = minify_json('{\n  "name": "张三",\n  "emoji": "😀"\n}')
        self.assertIn("张三", result)
        self.assertIn("😀", result)

    def test_empty_object(self):
        result = minify_json("{}")
        self.assertEqual(result, "{}")

    def test_empty_array(self):
        result = minify_json("[]")
        self.assertEqual(result, "[]")

    def test_array_root(self):
        result = minify_json("[\n  1,\n  2,\n  3\n]")
        self.assertEqual(result, "[1,2,3]")


class TestValidateJson(unittest.TestCase):
    """Tests for validate_json function."""

    def test_valid_json(self):
        result = validate_json('{"name":"John"}')
        self.assertTrue(result["valid"])
        self.assertIsNone(result["error"])

    def test_invalid_json(self):
        result = validate_json('{"name": "John",}')
        self.assertFalse(result["valid"])
        self.assertIsNotNone(result["error"])

    def test_primitive_string(self):
        result = validate_json('"hello"')
        self.assertTrue(result["valid"])

    def test_primitive_number(self):
        result = validate_json("123")
        self.assertTrue(result["valid"])

    def test_primitive_true(self):
        result = validate_json("true")
        self.assertTrue(result["valid"])

    def test_primitive_false(self):
        result = validate_json("false")
        self.assertTrue(result["valid"])

    def test_primitive_null(self):
        result = validate_json("null")
        self.assertTrue(result["valid"])

    def test_empty_string(self):
        result = validate_json("")
        self.assertFalse(result["valid"])

    def test_empty_object(self):
        result = validate_json("{}")
        self.assertTrue(result["valid"])

    def test_empty_array(self):
        result = validate_json("[]")
        self.assertTrue(result["valid"])

    def test_nested_structure(self):
        result = validate_json('{"a":{"b":[1,2,3]}}')
        self.assertTrue(result["valid"])


class TestGetJsonSize(unittest.TestCase):
    """Tests for get_json_size function."""

    def test_ascii_size(self):
        json_str = '{"name":"John"}'
        result = get_json_size(json_str)
        self.assertEqual(result, len(json_str.encode("utf-8")))

    def test_unicode_size(self):
        json_str = '{"name":"张三"}'
        result = get_json_size(json_str)
        self.assertEqual(result, len(json_str.encode("utf-8")))

    def test_empty_object(self):
        json_str = "{}"
        result = get_json_size(json_str)
        self.assertEqual(result, 2)

    def test_invalid_json_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            get_json_size("{bad}")
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_array_size(self):
        json_str = "[1,2,3]"
        result = get_json_size(json_str)
        self.assertEqual(result, len(json_str.encode("utf-8")))


class TestGetJsonLineCount(unittest.TestCase):
    """Tests for get_json_line_count function."""

    def test_multi_line(self):
        json_str = '{\n  "a": 1,\n  "b": 2\n}'
        result = get_json_line_count(json_str)
        self.assertEqual(result, 4)

    def test_single_line(self):
        json_str = '{"a":1}'
        result = get_json_line_count(json_str)
        self.assertEqual(result, 1)

    def test_empty_string(self):
        result = get_json_line_count("")
        self.assertEqual(result, 0)

    def test_whitespace_only(self):
        result = get_json_line_count("   \n  \t  ")
        self.assertEqual(result, 0)

    def test_invalid_json_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            get_json_line_count("{bad}")
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_array_root(self):
        json_str = "[\n  1,\n  2\n]"
        result = get_json_line_count(json_str)
        self.assertEqual(result, 4)


class TestValidateColumnOrder(unittest.TestCase):
    """Tests for validate_column_order function."""

    def _make_datax(self, reader_cols, writer_cols):
        return json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": reader_cols}},
                    "writer": {"parameter": {"column": writer_cols}},
                }]
            }
        })

    def test_matching_columns(self):
        js = self._make_datax(
            ["`id`", "`name`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        result = validate_column_order(js)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["results"]), 1)
        self.assertTrue(result["results"][0]["valid"])
        self.assertEqual(result["results"][0]["mismatches"], [])
        self.assertEqual(result["results"][0]["reader_count"], 2)
        self.assertEqual(result["results"][0]["writer_count"], 2)

    def test_mismatched_columns(self):
        js = self._make_datax(
            ["`id`", "`age`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        mismatches = result["results"][0]["mismatches"]
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["position"], 2)
        self.assertEqual(mismatches[0]["reader_field"], "age")
        self.assertEqual(mismatches[0]["writer_field"], "name")

    def test_reader_longer_than_writer(self):
        js = self._make_datax(
            ["`a`", "`b`", "`c`"],
            [{"name": "x", "type": "bigint"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        r = result["results"][0]
        self.assertEqual(r["reader_count"], 3)
        self.assertEqual(r["writer_count"], 1)
        self.assertEqual(len(r["mismatches"]), 3)

    def test_writer_longer_than_reader(self):
        js = self._make_datax(
            ["`id`"],
            [{"name": "id"}, {"name": "name"}, {"name": "extra"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        r = result["results"][0]
        self.assertEqual(r["reader_count"], 1)
        self.assertEqual(r["writer_count"], 3)

    def test_invalid_json_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            validate_column_order("{bad}")
        self.assertIn("Invalid JSON", str(ctx.exception))

    def test_non_dict_root(self):
        with self.assertRaises(ValueError) as ctx:
            validate_column_order("[1,2,3]")
        self.assertIn("JSON root must be an object", str(ctx.exception))

    def test_missing_job(self):
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"foo":"bar"}')
        self.assertIn("Missing or invalid 'job' field", str(ctx.exception))

    def test_missing_content(self):
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"job":{}}')
        self.assertIn("Missing or empty 'job.content' array", str(ctx.exception))

    def test_empty_content_array(self):
        with self.assertRaises(ValueError) as ctx:
            validate_column_order('{"job":{"content":[]}}')
        self.assertIn("Missing or empty 'job.content' array", str(ctx.exception))

    def test_multiple_content_items_all_match(self):
        js = json.dumps({
            "job": {
                "content": [
                    {
                        "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                        "writer": {"parameter": {"column": [{"name": "id"}, {"name": "name"}]}},
                    },
                    {
                        "reader": {"parameter": {"column": ["`age`", "`city`"]}},
                        "writer": {"parameter": {"column": [{"name": "age"}, {"name": "city"}]}},
                    },
                ]
            }
        })
        result = validate_column_order(js)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["results"]), 2)
        self.assertTrue(result["results"][0]["valid"])
        self.assertTrue(result["results"][1]["valid"])

    def test_multiple_content_one_mismatch(self):
        js = json.dumps({
            "job": {
                "content": [
                    {
                        "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                        "writer": {"parameter": {"column": [{"name": "id"}, {"name": "name"}]}},
                    },
                    {
                        "reader": {"parameter": {"column": ["`x`"]}},
                        "writer": {"parameter": {"column": [{"name": "y"}]}},
                    },
                ]
            }
        })
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        self.assertTrue(result["results"][0]["valid"])
        self.assertFalse(result["results"][1]["valid"])

    def test_writer_string_columns_backtick_stripped(self):
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                    "writer": {"parameter": {"column": ["id", "name"]}},
                }]
            }
        })
        result = validate_column_order(js)
        self.assertTrue(result["valid"])

    def test_writer_dict_columns_backtick_not_stripped(self):
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["id", "name"]}},
                    "writer": {"parameter": {"column": [{"name": "`id`"}, {"name": "`name`"}]}},
                }]
            }
        })
        result = validate_column_order(js)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["results"][0]["mismatches"]), 2)

    def test_case_sensitive_comparison(self):
        js = self._make_datax(
            ["ID", "Name"],
            [{"name": "id"}, {"name": "name"}],
        )
        result = validate_column_order(js)
        self.assertFalse(result["valid"])

    def test_special_characters_in_names(self):
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`user-id`", "`created_at`"]}},
                    "writer": {"parameter": {"column": [{"name": "user-id"}, {"name": "created_at"}]}},
                }]
            }
        })
        result = validate_column_order(js)
        self.assertTrue(result["valid"])


class TestExtractContent(unittest.TestCase):
    """Tests for _extract_content helper function."""

    def test_valid_structure(self):
        parsed = {"job": {"content": [{"reader": {}, "writer": {}}]}}
        result = _extract_content(parsed)
        self.assertEqual(result, [{"reader": {}, "writer": {}}])

    def test_non_dict_root(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content([1, 2, 3])
        self.assertIn("JSON root must be an object", str(ctx.exception))

    def test_missing_job(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content({"foo": "bar"})
        self.assertIn("Missing or invalid 'job' field", str(ctx.exception))

    def test_job_is_not_dict(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content({"job": "not_a_dict"})
        self.assertIn("Missing or invalid 'job' field", str(ctx.exception))

    def test_missing_content(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content({"job": {}})
        self.assertIn("Missing or empty 'job.content' array", str(ctx.exception))

    def test_content_is_not_list(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content({"job": {"content": "not_a_list"}})
        self.assertIn("Missing or empty 'job.content' array", str(ctx.exception))

    def test_content_is_empty_list(self):
        with self.assertRaises(ValueError) as ctx:
            _extract_content({"job": {"content": []}})
        self.assertIn("Missing or empty 'job.content' array", str(ctx.exception))

    def test_multiple_content_items(self):
        parsed = {"job": {"content": [{"a": 1}, {"b": 2}, {"c": 3}]}}
        result = _extract_content(parsed)
        self.assertEqual(len(result), 3)


class TestExtractReaderColumns(unittest.TestCase):
    """Tests for _extract_reader_columns helper function."""

    def test_strips_backticks(self):
        item = {"reader": {"parameter": {"column": ["`id`", "`name`", "`email`"]}}}
        result = _extract_reader_columns(item, 0)
        self.assertEqual(result, ["id", "name", "email"])

    def test_no_backticks(self):
        item = {"reader": {"parameter": {"column": ["id", "name"]}}}
        result = _extract_reader_columns(item, 0)
        self.assertEqual(result, ["id", "name"])

    def test_mixed_backticks(self):
        item = {"reader": {"parameter": {"column": ["`id`", "name", "`email`"]}}}
        result = _extract_reader_columns(item, 0)
        self.assertEqual(result, ["id", "name", "email"])

    def test_missing_reader(self):
        item = {"writer": {"parameter": {"column": []}}}
        with self.assertRaises(ValueError) as ctx:
            _extract_reader_columns(item, 0)
        self.assertIn("content[0]: missing 'reader.parameter.column'", str(ctx.exception))

    def test_missing_parameter(self):
        item = {"reader": {}}
        with self.assertRaises(ValueError) as ctx:
            _extract_reader_columns(item, 1)
        self.assertIn("content[1]: missing 'reader.parameter.column'", str(ctx.exception))

    def test_column_not_list(self):
        item = {"reader": {"parameter": {"column": "not_a_list"}}}
        with self.assertRaises(ValueError) as ctx:
            _extract_reader_columns(item, 0)
        self.assertIn("reader.parameter.column must be an array", str(ctx.exception))

    def test_empty_column_list(self):
        item = {"reader": {"parameter": {"column": []}}}
        result = _extract_reader_columns(item, 0)
        self.assertEqual(result, [])

    def test_index_in_error_message(self):
        item = {"reader": {}}
        with self.assertRaises(ValueError) as ctx:
            _extract_reader_columns(item, 5)
        self.assertIn("content[5]", str(ctx.exception))


class TestExtractWriterColumns(unittest.TestCase):
    """Tests for _extract_writer_columns helper function."""

    def test_dict_format(self):
        item = {
            "writer": {
                "parameter": {
                    "column": [
                        {"name": "id", "type": "bigint"},
                        {"name": "name", "type": "string"},
                    ]
                }
            }
        }
        result = _extract_writer_columns(item, 0)
        self.assertEqual(result, ["id", "name"])

    def test_string_format_strips_backticks(self):
        item = {"writer": {"parameter": {"column": ["`id`", "`name`"]}}}
        result = _extract_writer_columns(item, 0)
        self.assertEqual(result, ["id", "name"])

    def test_string_format_no_backticks(self):
        item = {"writer": {"parameter": {"column": ["id", "name"]}}}
        result = _extract_writer_columns(item, 0)
        self.assertEqual(result, ["id", "name"])

    def test_dict_format_preserves_backticks(self):
        item = {"writer": {"parameter": {"column": [{"name": "`id`"}, {"name": "`name`"}]}}}
        result = _extract_writer_columns(item, 0)
        self.assertEqual(result, ["`id`", "`name`"])

    def test_missing_writer(self):
        item = {"reader": {"parameter": {"column": []}}}
        with self.assertRaises(ValueError) as ctx:
            _extract_writer_columns(item, 0)
        self.assertIn("content[0]: missing 'writer.parameter.column'", str(ctx.exception))

    def test_column_not_list(self):
        item = {"writer": {"parameter": {"column": "not_a_list"}}}
        with self.assertRaises(ValueError) as ctx:
            _extract_writer_columns(item, 0)
        self.assertIn("writer.parameter.column must be an array", str(ctx.exception))

    def test_invalid_column_format(self):
        item = {"writer": {"parameter": {"column": [123, 456]}}}
        with self.assertRaises(ValueError) as ctx:
            _extract_writer_columns(item, 0)
        self.assertIn("writer.parameter.column[0] has invalid format", str(ctx.exception))

    def test_empty_column_list(self):
        item = {"writer": {"parameter": {"column": []}}}
        result = _extract_writer_columns(item, 0)
        self.assertEqual(result, [])

    def test_index_in_error_message(self):
        item = {"writer": {}}
        with self.assertRaises(ValueError) as ctx:
            _extract_writer_columns(item, 3)
        self.assertIn("content[3]", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
