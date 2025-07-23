"""Jikan/AioJikan Exceptions
====================================
exceptions.py contains exceptions used in Jikan and AioJikan.
"""
from typing import Optional, Mapping, Any, Union


class __typ1(Exception):
    """Base exception class for JikanPy."""


class __typ2(__typ1):
    """Exception due to an error response from Jikan API.

    Attributes:
        status_code: HTTP response status code.
        error_json: JSON error response from Jikan. Defaults to None.
        relevant_params: Relevant parameters passed into the method resulting in the
            exception.
    """

    def __init__(  # pylint: disable=too-many-arguments
        __tmp0,
        status_code: <FILL>,
        error_json: Optional[Mapping[str, Any]] = None,
        **relevant_params,
    ):
        __tmp0.status_code = status_code
        __tmp0.error_json = error_json
        __tmp0.relevant_params = relevant_params
        super().__init__(__tmp0.status_code)

    def __tmp1(__tmp0) -> str:
        output = f"HTTP {__tmp0.status_code}"
        if __tmp0.error_json:
            error_str = ", ".join(f"{k}={v}" for k, v in __tmp0.error_json.items())
            output += f" - {error_str}"
        if __tmp0.relevant_params:
            param_str = ", ".join(f"{k}={v}" for k, v in __tmp0.relevant_params.items())
            output += f" for {param_str}"
        return output

    def __repr__(__tmp0) :
        return (
            f"APIException(status_code={__tmp0.status_code}, "
            f"error_json={__tmp0.error_json}, relevant_params={__tmp0.relevant_params})"
        )


class __typ0(__typ1):
    """Exception raised when attempting to use deprecated API endpoints."""
