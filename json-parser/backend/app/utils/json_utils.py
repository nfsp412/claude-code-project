"""JSON utility functions for formatting, minifying, validating, and analyzing JSON."""

import json


def format_json(json_str: str, indent: int | str = 2) -> str:
    """
    Format a JSON string with proper indentation.

    Args:
        json_str: The JSON string to format
        indent: Number of spaces for indentation (default: 2), or "tab" for tab indentation

    Returns:
        Formatted JSON string

    Raises:
        ValueError: If the JSON string is invalid
    """
    try:
        parsed = json.loads(json_str)
        if indent == "tab":
            return json.dumps(parsed, indent="\t", ensure_ascii=False)
        return json.dumps(parsed, indent=indent, ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def minify_json(json_str: str) -> str:
    """
    Minify a JSON string by removing all whitespace.

    Args:
        json_str: The JSON string to minify

    Returns:
        Minified JSON string

    Raises:
        ValueError: If the JSON string is invalid
    """
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def validate_json(json_str: str) -> dict:
    """
    Validate a JSON string.

    Args:
        json_str: The JSON string to validate

    Returns:
        A dictionary with 'valid' boolean and optional 'error' message
    """
    try:
        json.loads(json_str)
        return {"valid": True, "error": None}
    except json.JSONDecodeError as e:
        return {"valid": False, "error": str(e)}


def get_json_size(json_str: str) -> int:
    """
    Get the size of a JSON string in bytes.

    Args:
        json_str: The JSON string to measure

    Returns:
        Size in bytes

    Raises:
        ValueError: If the JSON string is invalid
    """
    try:
        json.loads(json_str)
        return len(json_str.encode('utf-8'))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def get_json_line_count(json_str: str) -> int:
    """
    Get the number of lines in a JSON string.

    Args:
        json_str: The JSON string to count lines

    Returns:
        Number of lines (0 for empty string)

    Raises:
        ValueError: If the JSON string is invalid
    """
    if not json_str or not json_str.strip():
        return 0

    try:
        json.loads(json_str)
        lines = json_str.strip().split('\n')
        return len(lines)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
