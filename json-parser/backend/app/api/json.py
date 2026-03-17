"""JSON API routes for FastAPI application."""

from typing import Literal, Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.utils.json_utils import (
    format_json,
    minify_json,
    validate_json,
    get_json_size,
    get_json_line_count,
    validate_column_order,
)

router = APIRouter(prefix="/api/json", tags=["json"])


class JsonRequest(BaseModel):
    """Request model for JSON operations."""
    json_str: str = Field(..., alias="json", description="The JSON string to process")


class JsonFormatRequest(BaseModel):
    """Request model for JSON format operation with optional indent."""
    json_str: str = Field(..., alias="json", description="The JSON string to format")
    indent: Union[int, Literal["tab"]] = Field(default=2, description="Indentation: 1, 2, 4, 8, or 'tab'")


class FormatResponse(BaseModel):
    """Response model for format operation."""
    formatted: str = Field(..., description="The formatted JSON string")


class MinifyResponse(BaseModel):
    """Response model for minify operation."""
    minified: str = Field(..., description="The minified JSON string")


class ValidateResponse(BaseModel):
    """Response model for validate operation."""
    valid: bool = Field(..., description="Whether the JSON is valid")
    error: str | None = Field(None, description="Error message if invalid")


class SizeResponse(BaseModel):
    """Response model for size operation."""
    size: int = Field(..., description="Size in bytes")


class LinesResponse(BaseModel):
    """Response model for lines operation."""
    lines: int = Field(..., description="Number of lines")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")


class ColumnMismatch(BaseModel):
    """A single column position where reader and writer differ."""
    position: int = Field(..., description="1-based position index")
    reader_field: str | None = Field(None, description="Reader column name (None if missing)")
    writer_field: str | None = Field(None, description="Writer column name (None if missing)")


class ContentValidateResult(BaseModel):
    """Validation result for a single content item."""
    index: int = Field(..., description="Index in the content array")
    valid: bool
    reader_count: int
    writer_count: int
    mismatches: list[ColumnMismatch]


class ColumnValidateResponse(BaseModel):
    """Response model for column order validation."""
    valid: bool = Field(..., description="True if all content items have matching column order")
    results: list[ContentValidateResult]


@router.post("/format", response_model=FormatResponse, responses={400: {"model": ErrorResponse}})
async def format_endpoint(request: JsonFormatRequest):
    """
    Format a JSON string with proper indentation.

    - **json**: The JSON string to format
    - **indent**: Optional indentation (default: 2, options: 1, 2, 4, 8, 'tab')
    """
    try:
        formatted = format_json(request.json_str, request.indent)
        return FormatResponse(formatted=formatted)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/minify", response_model=MinifyResponse, responses={400: {"model": ErrorResponse}})
async def minify_endpoint(request: JsonRequest):
    """
    Minify a JSON string by removing all whitespace.

    - **json**: The JSON string to minify
    """
    try:
        minified = minify_json(request.json_str)
        return MinifyResponse(minified=minified)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate", response_model=ValidateResponse)
async def validate_endpoint(request: JsonRequest):
    """
    Validate a JSON string.

    - **json**: The JSON string to validate

    Returns valid=true if the JSON is valid, valid=false with error message otherwise.
    """
    result = validate_json(request.json_str)
    return ValidateResponse(valid=result["valid"], error=result["error"])


@router.post("/size", response_model=SizeResponse, responses={400: {"model": ErrorResponse}})
async def size_endpoint(request: JsonRequest):
    """
    Calculate the size of a JSON string in bytes.

    - **json**: The JSON string to measure
    """
    try:
        size = get_json_size(request.json_str)
        return SizeResponse(size=size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lines", response_model=LinesResponse, responses={400: {"model": ErrorResponse}})
async def lines_endpoint(request: JsonRequest):
    """
    Calculate the number of lines in a JSON string.

    - **json**: The JSON string to count lines
    """
    try:
        lines = get_json_line_count(request.json_str)
        return LinesResponse(lines=lines)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/validate-columns",
    response_model=ColumnValidateResponse,
    responses={400: {"model": ErrorResponse}},
)
async def validate_columns_endpoint(request: JsonRequest):
    """
    Validate that reader and writer column orders match in a DataX job config.

    - **json**: A DataX job configuration JSON string
    """
    try:
        result = validate_column_order(request.json_str)
        return ColumnValidateResponse(
            valid=result["valid"],
            results=[
                ContentValidateResult(
                    index=r["index"],
                    valid=r["valid"],
                    reader_count=r["reader_count"],
                    writer_count=r["writer_count"],
                    mismatches=[ColumnMismatch(**m) for m in r["mismatches"]],
                )
                for r in result["results"]
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
