"""Unit tests for JSON API endpoints."""

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


if __name__ == "__main__":
    unittest.main()
