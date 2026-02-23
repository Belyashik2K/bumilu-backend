from collections.abc import Mapping
from typing import (
    Any,
)

from pydantic import (
    BaseModel,
    Field,
)


class ErrorResponseSchema(BaseModel):
    error_message: str = Field(
        ...,
        description="A human-readable message describing the error.",
        examples=["I'm a teapot. You are a teapot. We are all teapots."],
    )
    details: Mapping[str, Any] = Field(
        {},
        description="Additional details about the error.",
        examples=[{"tea": "pot"}],
    )


class ValidationErrorResponseSchema(ErrorResponseSchema):
    details: Mapping[str, Any] = Field(
        ...,
        description="Additional details about the validation error.",
        examples=[
            {
                "validation_errors": [
                    {
                        "field": "email",
                        "location": "body",
                        "message": "value is not a valid email address",
                        "type": "value_error",
                    }
                ]
            }
        ],
    )
