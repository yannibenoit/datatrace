"""DataTrace Custom Exceptions.

Custom exception classes for error handling throughout DataTrace.
"""

from typing import Optional


class DataTraceError(Exception):
    """Base exception for all DataTrace errors."""

    def __init__(self, message: str, code: Optional[str] = None):
        """Initialize DataTrace error.

        Args:
            message: Error message
            code: Optional error code
        """
        self.message = message
        self.code = code
        super().__init__(message)


class ConfigurationError(DataTraceError):
    """Configuration-related errors."""

    def __init__(self, message: str, config_key: Optional[str] = None):
        """Initialize configuration error.

        Args:
            message: Error message
            config_key: The configuration key that caused the error
        """
        self.config_key = config_key
        super().__init__(message, code="CONFIG_ERROR")


class ConnectionError(DataTraceError):
    """Connection-related errors."""

    def __init__(self, message: str, connection_type: Optional[str] = None):
        """Initialize connection error.

        Args:
            message: Error message
            connection_type: The type of connection that failed
        """
        self.connection_type = connection_type
        super().__init__(message, code="CONNECTION_ERROR")


class DiscoveryError(DataTraceError):
    """Discovery-related errors."""

    def __init__(self, message: str, resource_type: Optional[str] = None):
        """Initialize discovery error.

        Args:
            message: Error message
            resource_type: The type of resource being discovered
        """
        self.resource_type = resource_type
        super().__init__(message, code="DISCOVERY_ERROR")


class LineageError(DataTraceError):
    """Lineage-related errors."""

    def __init__(self, message: str, relationship_type: Optional[str] = None):
        """Initialize lineage error.

        Args:
            message: Error message
            relationship_type: The type of lineage relationship
        """
        self.relationship_type = relationship_type
        super().__init__(message, code="LINEAGE_ERROR")


class ValidationError(DataTraceError):
    """Validation-related errors."""

    def __init__(self, message: str, field: Optional[str] = None):
        """Initialize validation error.

        Args:
            message: Error message
            field: The field that failed validation
        """
        self.field = field
        super().__init__(message, code="VALIDATION_ERROR")


class AuthenticationError(DataTraceError):
    """Authentication-related errors."""

    def __init__(self, message: str, provider: Optional[str] = None):
        """Initialize authentication error.

        Args:
            message: Error message
            provider: The authentication provider
        """
        self.provider = provider
        super().__init__(message, code="AUTH_ERROR")


class RateLimitError(DataTraceError):
    """Rate limit exceeded errors."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        """Initialize rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retry
        """
        self.retry_after = retry_after
        super().__init__(message, code="RATE_LIMIT_ERROR")
