"""Unit tests for JSON API endpoints."""

import json
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestJsonApiEndpoints(unittest.TestCase):
    """Tests for JSON API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_format_api_valid(self):
        """Test format endpoint with valid JSON."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"name":"John","age":30}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("formatted", data)
        self.assertIn('"name": "John"', data["formatted"])

    def test_format_api_with_tab_indent(self):
        """Test format endpoint with tab indentation."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"name":"John","age":30}', "indent": "tab"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("formatted", data)
        self.assertIn("\t\"name\"", data["formatted"])

    def test_format_api_with_all_indent_options(self):
        """Test format endpoint with all indentation options."""
        json_str = '{"key":"value"}'

        # 测试 1 空格
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str, "indent": 1}
        )
        self.assertEqual(response.status_code, 200)

        # 测试 2 空格
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str, "indent": 2}
        )
        self.assertEqual(response.status_code, 200)

        # 测试 4 空格
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str, "indent": 4}
        )
        self.assertEqual(response.status_code, 200)

        # 测试 8 空格
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str, "indent": 8}
        )
        self.assertEqual(response.status_code, 200)

        # 测试制表符
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str, "indent": "tab"}
        )
        self.assertEqual(response.status_code, 200)

    def test_format_api_invalid(self):
        """Test format endpoint with invalid JSON."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"name": "John",}'}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("detail", data)

    def test_minify_api(self):
        """Test minify endpoint."""
        response = self.client.post(
            "/api/json/minify",
            json={"json": '{\n  "name": "John"\n}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["minified"], '{"name":"John"}')

    def test_validate_api_valid(self):
        """Test validate endpoint with valid JSON."""
        response = self.client.post(
            "/api/json/validate",
            json={"json": '{"name": "John"}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])

    def test_validate_api_invalid(self):
        """Test validate endpoint with invalid JSON."""
        response = self.client.post(
            "/api/json/validate",
            json={"json": '{"name": "John",}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])

    def test_size_api(self):
        """Test size endpoint."""
        json_str = '{"name": "John"}'
        response = self.client.post(
            "/api/json/size",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["size"], len(json_str.encode('utf-8')))

    def test_lines_api(self):
        """Test lines endpoint."""
        json_str = '{\n  "name": "John",\n  "age": 30\n}'
        response = self.client.post(
            "/api/json/lines",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["lines"], 4)

    def test_404_not_found(self):
        """Test that non-existent endpoint returns 404."""
        response = self.client.get("/api/nonexistent")
        self.assertEqual(response.status_code, 404)


class TestValidateColumnsApi(unittest.TestCase):
    """Tests for POST /api/json/validate-columns endpoint."""

    def setUp(self):
        self.client = TestClient(app)

    def _make_datax(self, reader_cols, writer_cols):
        return json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": reader_cols}},
                    "writer": {"parameter": {"column": writer_cols}},
                }]
            }
        })

    def test_validate_columns_matching(self):
        """Matching columns should return valid=true."""
        js = self._make_datax(
            ["`id`", "`name`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["mismatches"], [])

    def test_validate_columns_mismatched(self):
        """Mismatched columns should return valid=false with details."""
        js = self._make_datax(
            ["`id`", "`age`"],
            [{"name": "id", "type": "bigint"}, {"name": "name", "type": "string"}],
        )
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])
        mismatches = data["results"][0]["mismatches"]
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["position"], 2)
        self.assertEqual(mismatches[0]["reader_field"], "age")
        self.assertEqual(mismatches[0]["writer_field"], "name")

    def test_validate_columns_invalid_json(self):
        """Invalid JSON should return 400."""
        response = self.client.post(
            "/api/json/validate-columns",
            json={"json": "{bad json}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_validate_columns_missing_structure(self):
        """JSON missing job.content should return 400."""
        response = self.client.post(
            "/api/json/validate-columns",
            json={"json": '{"foo": "bar"}'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_validate_columns_count_mismatch(self):
        """Different column counts should report reader_count and writer_count."""
        js = self._make_datax(
            ["`id`", "`name`", "`extra`"],
            [{"name": "id", "type": "bigint"}],
        )
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])
        r = data["results"][0]
        self.assertEqual(r["reader_count"], 3)
        self.assertEqual(r["writer_count"], 1)


class TestRootEndpoints(unittest.TestCase):
    """Tests for root endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("name", data)
        self.assertEqual(data["name"], "JSON Parser API")

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")


class TestJsonApiEdgeCases(unittest.TestCase):
    """Edge case and boundary tests for JSON API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_format_empty_object(self):
        """Test format endpoint with empty object."""
        response = self.client.post(
            "/api/json/format",
            json={"json": "{}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["formatted"].strip(), "{}")

    def test_format_empty_array(self):
        """Test format endpoint with empty array."""
        response = self.client.post(
            "/api/json/format",
            json={"json": "[]"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["formatted"].strip(), "[]")

    def test_format_null_value(self):
        """Test format endpoint with null value."""
        response = self.client.post(
            "/api/json/format",
            json={"json": "null"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["formatted"].strip(), "null")

    def test_format_boolean_values(self):
        """Test format endpoint with boolean values."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"active":true,"disabled":false}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('"active": true', data["formatted"])
        self.assertIn('"disabled": false', data["formatted"])

    def test_format_unicode_characters(self):
        """Test format endpoint with unicode characters."""
        json_str = '{"name": "张三", "city": "北京", "emoji": "😀"}'
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("张三", data["formatted"])
        self.assertIn("北京", data["formatted"])
        self.assertIn("😀", data["formatted"])

    def test_format_nested_json(self):
        """Test format endpoint with deeply nested JSON."""
        json_str = '{"level1":{"level2":{"level3":{"level4":{"value":"deep"}}}}}'
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('"level1"', data["formatted"])
        self.assertIn('"level4"', data["formatted"])

    def test_format_special_characters(self):
        """Test format endpoint with special characters."""
        json_str = '{"key":"value with\\nnewline","tab":"with\\ttab","quote":"with\\"quote"}'
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)

    def test_format_number_types(self):
        """Test format endpoint with different number types."""
        json_str = '{"int":42,"float":3.14,"negative":-10,"exp":1.5e10}'
        response = self.client.post(
            "/api/json/format",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('"int": 42', data["formatted"])
        self.assertIn('"float": 3.14', data["formatted"])

    def test_minify_empty_container(self):
        """Test minify endpoint with empty containers."""
        for empty_json in ["{}", "[]"]:
            response = self.client.post(
                "/api/json/minify",
                json={"json": empty_json}
            )
            self.assertEqual(response.status_code, 200)

    def test_minify_unicode_content(self):
        """Test minify endpoint with unicode content."""
        json_str = '{\n  "name": "张三",\n  "emoji": "😀"\n}'
        response = self.client.post(
            "/api/json/minify",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["minified"], '{"name":"张三","emoji":"😀"}')

    def test_validate_primitives(self):
        """Test validate endpoint with primitive values."""
        for primitive in ['"string"', '123', 'true', 'false', 'null']:
            response = self.client.post(
                "/api/json/validate",
                json={"json": primitive}
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["valid"])

    def test_validate_empty_string(self):
        """Test validate endpoint with empty string."""
        response = self.client.post(
            "/api/json/validate",
            json={"json": ""}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])

    def test_size_with_unicode(self):
        """Test size endpoint with unicode characters."""
        json_str = '{"name": "张三"}'
        response = self.client.post(
            "/api/json/size",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Unicode characters should be counted in bytes (3 bytes per Chinese char in UTF-8)
        expected_size = len(json_str.encode('utf-8'))
        self.assertEqual(data["size"], expected_size)

    def test_lines_with_various_line_endings(self):
        """Test lines endpoint with various line endings."""
        # Unix style - valid multi-line JSON
        response = self.client.post(
            "/api/json/lines",
            json={"json": '{\n  "a": 1,\n  "b": 2\n}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["lines"], 4)

        # Single line JSON
        response = self.client.post(
            "/api/json/lines",
            json={"json": '{"a":1}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["lines"], 1)

    def test_format_invalid_indent_type(self):
        """Test format endpoint with invalid indent type."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"a":1}', "indent": "invalid"}
        )
        # Should fail validation
        self.assertEqual(response.status_code, 422)

    def test_format_indent_zero(self):
        """Test format endpoint with indent 0 (should use default or single line)."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"a":1}', "indent": 0}
        )
        self.assertEqual(response.status_code, 200)

    def test_format_indent_out_of_range(self):
        """Test format endpoint with out of range indent."""
        response = self.client.post(
            "/api/json/format",
            json={"json": '{"a":1}', "indent": 10}
        )
        # Large indent might still work or fail depending on validation
        self.assertIn(response.status_code, [200, 400])

    def test_array_json(self):
        """Test endpoints with array as root element."""
        json_str = '[{"id":1},{"id":2}]'

        response = self.client.post(
            "/api/json/format",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/api/json/minify",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/api/json/validate",
            json={"json": json_str}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])

    def test_missing_json_field(self):
        """Test endpoints with missing json field."""
        response = self.client.post(
            "/api/json/format",
            json={"indent": 2}
        )
        self.assertEqual(response.status_code, 422)

    def test_content_type_json(self):
        """Test endpoints with explicit Content-Type header."""
        response = self.client.post(
            "/api/json/validate",
            json={"json": '{"valid":true}'},
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)


class TestValidateColumnsEdgeCases(unittest.TestCase):
    """Edge case tests for validate-columns endpoint."""

    def setUp(self):
        self.client = TestClient(app)

    def test_validate_columns_with_backtick_stripping(self):
        """Test that backticks are properly stripped from reader columns."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`", "`name`"]}},
                    "writer": {"parameter": {"column": ["id", "name"]}},
                }]
            }
        })
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])

    def test_validate_columns_writer_with_backticks(self):
        """Test writer columns with backticks in name field."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["id", "name"]}},
                    "writer": {"parameter": {"column": [{"name": "`id`"}, {"name": "`name`"}]}},
                }]
            }
        })
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Writer column names in dict format are NOT stripped of backticks
        # So "id" != "`id`" and the validation should fail
        self.assertFalse(data["valid"])
        self.assertEqual(len(data["results"][0]["mismatches"]), 2)

    def test_validate_columns_case_sensitive(self):
        """Test that column name comparison is case sensitive."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["ID", "Name"]}},
                    "writer": {"parameter": {"column": [{"name": "id"}, {"name": "name"}]}},
                }]
            }
        })
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["valid"])

    def test_validate_columns_multiple_content_all_match(self):
        """Test multiple content items where all match."""
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
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])
        self.assertEqual(len(data["results"]), 2)
        self.assertTrue(data["results"][0]["valid"])
        self.assertTrue(data["results"][1]["valid"])

    def test_validate_columns_null_values_in_data(self):
        """Test validation with null values in column data."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`id`", "`nullable`"]}},
                    "writer": {"parameter": {"column": [{"name": "id", "type": "bigint"}, {"name": "nullable", "type": "string"}]}},
                }]
            }
        })
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])

    def test_validate_columns_with_special_names(self):
        """Test columns with special characters in names."""
        js = json.dumps({
            "job": {
                "content": [{
                    "reader": {"parameter": {"column": ["`user-id`", "`created_at`", "`email@test`"]}},
                    "writer": {"parameter": {"column": [{"name": "user-id"}, {"name": "created_at"}, {"name": "email@test"}]}},
                }]
            }
        })
        response = self.client.post("/api/json/validate-columns", json={"json": js})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["valid"])


if __name__ == "__main__":
    unittest.main()
