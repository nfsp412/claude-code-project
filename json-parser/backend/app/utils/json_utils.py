"""JSON utility functions for formatting, minifying, validating, and analyzing JSON."""

import json
from itertools import zip_longest


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


def validate_column_order(json_str: str) -> dict:
    """
    Validate that reader and writer column orders match in a DataX job config.

    Compares job.content[*].reader.parameter.column (string list with backticks)
    against job.content[*].writer.parameter.column (object list with name/type).

    Args:
        json_str: A JSON string containing a DataX job configuration

    Returns:
        A dict with 'valid' (bool) and 'results' (list of per-content validation details)

    Raises:
        ValueError: If the JSON is invalid or missing required structure
    """
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    content = _extract_content(parsed)

    all_valid = True
    results = []

    for idx, item in enumerate(content):
        reader_columns = _extract_reader_columns(item, idx)
        writer_columns = _extract_writer_columns(item, idx)

        mismatches = []
        for pos, (r, w) in enumerate(zip_longest(reader_columns, writer_columns), start=1):
            if r != w:
                mismatches.append({
                    "position": pos,
                    "reader_field": r,
                    "writer_field": w,
                })

        item_valid = len(mismatches) == 0
        if not item_valid:
            all_valid = False

        results.append({
            "index": idx,
            "valid": item_valid,
            "reader_count": len(reader_columns),
            "writer_count": len(writer_columns),
            "mismatches": mismatches,
        })

    return {"valid": all_valid, "results": results}


def _extract_content(parsed: dict) -> list:
    """Extract and validate the job.content array from parsed JSON."""
    if not isinstance(parsed, dict):
        raise ValueError("JSON root must be an object")
    job = parsed.get("job")
    if not isinstance(job, dict):
        raise ValueError("Missing or invalid 'job' field")
    content = job.get("content")
    if not isinstance(content, list) or len(content) == 0:
        raise ValueError("Missing or empty 'job.content' array")
    return content


def _extract_reader_columns(item: dict, idx: int) -> list[str]:
    """Extract cleaned column names from a content item's reader."""
    try:
        columns = item["reader"]["parameter"]["column"]
    except (KeyError, TypeError):
        raise ValueError(
            f"content[{idx}]: missing 'reader.parameter.column'"
        )
    if not isinstance(columns, list):
        raise ValueError(f"content[{idx}]: reader.parameter.column must be an array")
    return [col.strip("`") for col in columns]


def _extract_writer_columns(item: dict, idx: int) -> list[str]:
    """Extract column names from a content item's writer."""
    try:
        columns = item["writer"]["parameter"]["column"]
    except (KeyError, TypeError):
        raise ValueError(
            f"content[{idx}]: missing 'writer.parameter.column'"
        )
    if not isinstance(columns, list):
        raise ValueError(f"content[{idx}]: writer.parameter.column must be an array")
    result = []
    for i, col in enumerate(columns):
        if isinstance(col, dict) and "name" in col:
            result.append(col["name"])
        elif isinstance(col, str):
            result.append(col.strip("`"))
        else:
            raise ValueError(
                f"content[{idx}]: writer.parameter.column[{i}] has invalid format"
            )
    return result
