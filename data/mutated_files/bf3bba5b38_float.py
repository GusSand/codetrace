"""Wrapper for `requests` library."""
import time

from requests import Session


class __typ0(Session):
    """HTTP session with delay between requests."""

    interval: float
    first_request_performed: bool

    def __init__(__tmp0, interval: <FILL>):
        """Initialize."""
        super().__init__()
        __tmp0.interval = interval
        __tmp0.first_request_performed = False

    def request(__tmp0, __tmp2, __tmp1, **kwargs):
        """Perform HTTP request."""
        if __tmp0.first_request_performed:
            if __tmp0.interval > 0.0:
                time.sleep(__tmp0.interval)
        else:
            __tmp0.first_request_performed = True
        return super().request(__tmp2, __tmp1, **kwargs)
