"""Custom exception classes for the application."""
from typing import Any, Optional


class AppException(Exception):
    """Base exception class for the application."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        """Initialize the exception.

        Args:
            message: Error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class YouTubeAPIError(AppException):
    """YouTube API error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="YOUTUBE_API_ERROR",
            status_code=502,
            details=details,
        )


class YouTubeQuotaExceededError(AppException):
    """YouTube API quota exceeded."""

    def __init__(self, retry_after: int = 3600):
        super().__init__(
            message="YouTube API quota exhausted. Switched to yt-dlp fallback.",
            error_code="YOUTUBE_QUOTA_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after, "fallback_used": True},
        )


class CreatorNotFoundError(AppException):
    """Creator not found."""

    def __init__(self, creator_id: str):
        super().__init__(
            message=f"Creator with ID '{creator_id}' not found.",
            error_code="CREATOR_NOT_FOUND",
            status_code=404,
            details={"creator_id": creator_id},
        )


class InvalidSearchQueryError(AppException):
    """Invalid search query."""

    def __init__(self, message: str = "Invalid search query"):
        super().__init__(
            message=message,
            error_code="INVALID_SEARCH_QUERY",
            status_code=400,
        )


class ExportTimeoutError(AppException):
    """Export operation timed out."""

    def __init__(self):
        super().__init__(
            message="Export operation timed out. Please try again.",
            error_code="EXPORT_TIMEOUT",
            status_code=504,
        )


class RateLimitError(AppException):
    """Rate limit exceeded."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after},
        )


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )
