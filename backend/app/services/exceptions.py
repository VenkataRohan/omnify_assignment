"""
Custom exceptions for service layer.
"""


class ServiceError(Exception):
    """Base exception for service layer errors."""
    pass


class NotFoundError(ServiceError):
    """Exception raised when a resource is not found."""
    pass


class AlreadyExistsError(ServiceError):
    """Exception raised when a resource already exists."""
    pass


class ValidationError(ServiceError):
    """Exception raised when validation fails."""
    pass


class CapacityError(ServiceError):
    """Exception raised when capacity limits are exceeded."""
    pass


# Event-specific exceptions
class EventNotFoundError(NotFoundError):
    """Exception raised when an event is not found."""
    pass


class EventAlreadyExistsError(AlreadyExistsError):
    """Exception raised when an event already exists."""
    pass


class EventValidationError(ValidationError):
    """Exception raised when event validation fails."""
    pass


class EventCapacityExceededError(CapacityError):
    """Exception raised when event capacity is exceeded."""
    pass


# Attendee-specific exceptions
class AttendeeNotFoundError(NotFoundError):
    """Exception raised when an attendee is not found."""
    pass


class AttendeeAlreadyRegisteredError(AlreadyExistsError):
    """Exception raised when an attendee is already registered."""
    pass


class AttendeeValidationError(ValidationError):
    """Exception raised when attendee validation fails."""
    pass
