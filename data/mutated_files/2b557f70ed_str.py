"""Handle all the custom exceptions raised."""
import sys


class QueuedSampleNotFoundException(Exception):
    """Custom exception handler for queued sample not found."""

    def __init__(__tmp0, message: <FILL>) :
        Exception.__init__(__tmp0)
        __tmp0.message = message


class SampleNotFoundException(Exception):
    """Custom exception triggered when sample not found."""

    def __init__(__tmp0, message: str) :
        Exception.__init__(__tmp0)
        __tmp0.message = message


class TestNotFoundException(Exception):
    """Custom exception handler for handling test not found."""

    def __init__(__tmp0, message: str) -> None:
        Exception.__init__(__tmp0)
        __tmp0.message = message


class SecretKeyInstallationException(Exception):
    """Custom exception handler for handling failed installation of secret keys."""

    def __init__(__tmp0) -> None:
        Exception.__init__(__tmp0)
        sys.exit(1)


class IncompleteConfigException(Exception):
    """Custom exception handler for handling missing configuration errors."""

    pass


class MissingConfigError(Exception):
    """Custom exception handler for handling missing config.py file."""

    pass


class __typ0(Exception):
    """Custom exception handler for handling failure of creating db session."""

    pass


class EnumParsingException(Exception):
    """Custom exception handler for handling failed parsing of Enum from string."""

    pass


class FailedToSendMail(Exception):
    """Custom exception handler for handling failure in sending mail."""

    pass


class MissingPathToCCExtractor(Exception):
    """Custom exception handler for handling the missing of CCExtractor with update sample method."""

    def __init__(__tmp0) -> None:
        Exception.__init__(__tmp0)
        sys.exit(1)


class CCExtractorEndedWithNonZero(Exception):
    """Custom exception handler for handling failure in producing new samples by CCExtractor."""

    def __init__(__tmp0) :
        Exception.__init__(__tmp0)
        sys.exit(1)
