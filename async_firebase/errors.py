"""Async Firebase errors."""
import typing as t
from enum import Enum

import httpx


class FcmErrorCode(Enum):
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    FAILED_PRECONDITION = "FAILED_PRECONDITION"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    ABORTED = "ABORTED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
    CANCELLED = "CANCELLED"
    DATA_LOSS = "DATA_LOSS"
    UNKNOWN = "UNKNOWN"
    INTERNAL = "INTERNAL"
    UNAVAILABLE = "UNAVAILABLE"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"


class BaseAsyncFirebaseError(Exception):
    """Base error for Async Firebase"""


class AsyncFirebaseError(BaseAsyncFirebaseError):
    """A prototype for all AF Errors.

    This error and its subtypes and the reason to rise them are consistent with Google's errors,
    that may be found in `firebase-admin-python` in `firebase_admin.exceptions module`.
    """

    def __init__(
        self,
        code: str,
        message: str,
        cause: t.Optional[Exception] = None,
        http_response: t.Optional[httpx.Response] = None,
    ):
        """Init the AsyncFirebase error.

        :param code: A string error code that represents the type of the exception. Possible error
            codes are defined in https://cloud.google.com/apis/design/errors#handling_errors.
        :param message: A human-readable error message string.
        :param cause: The exception that caused this error (optional).
        :param http_response: If this error was caused by an HTTP error response, this property is
            set to the ``httpx.Response`` object that represents the HTTP response (optional).
            See https://www.python-httpx.org/api/#response for details of this object.
        """
        self.code = code
        self.cause = cause
        self.http_response = http_response
        super().__init__(self, message)


class DeadlineExceededError(AsyncFirebaseError):
    """Request deadline exceeded.

    This will happen only if the caller sets a deadline that is shorter than the method's
    default deadline (i.e. requested deadline is not enough for the server to process the
    request) and the request did not finish within the deadline.
    """

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.DEADLINE_EXCEEDED.value, message, cause=cause, http_response=http_response)


class UnavailableError(AsyncFirebaseError):
    """Service unavailable. Typically the server is down."""

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.UNAVAILABLE.value, message, cause=cause, http_response=http_response)


class UnknownError(AsyncFirebaseError):
    """Unknown server error."""

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.UNKNOWN.value, message, cause=cause, http_response=http_response)


class UnauthenticatedError(AsyncFirebaseError):
    """Request not authenticated due to missing, invalid, or expired OAuth token."""

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.UNAUTHENTICATED.value, message, cause=cause, http_response=http_response)


class ThirdPartyAuthError(UnauthenticatedError):
    """APNs certificate or web push auth key was invalid or missing."""


class ResourceExhaustedError(AsyncFirebaseError):
    """Either out of resource quota or reaching rate limiting."""

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.RESOURCE_EXHAUSTED.value, message, cause=cause, http_response=http_response)


class QuotaExceededError(ResourceExhaustedError):
    """Sending limit exceeded for the message target."""


class PermissionDeniedError(AsyncFirebaseError):
    """Client does not have sufficient permission.

    This can happen because the OAuth token does not have the right scopes, the client doesn't
    have permission, or the API has not been enabled for the client project.
    """

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.PERMISSION_DENIED.value, message, cause=cause, http_response=http_response)


class SenderIdMismatchError(PermissionDeniedError):
    """The authenticated sender ID is different from the sender ID for the registration token."""


class NotFoundError(AsyncFirebaseError):
    """A specified resource is not found, or the request is rejected by undisclosed reasons.

    An example of the possible cause of theis error is whitelisting.
    """

    def __init__(self, message, cause=None, http_response=None):
        """Please see params information in the base exception docstring."""
        super().__init__(self, FcmErrorCode.NOT_FOUND.value, message, cause=cause, http_response=http_response)


class UnregisteredError(NotFoundError):
    """App instance was unregistered from FCM.

    This usually means that the token used is no longer valid and a new one must be used.
    """
