"""Custom exceptions for the Student Information System."""


class SISError(Exception):
    """Base class for all application errors."""


class ValidationError(SISError):
    """Raised when student data is invalid."""


class StudentNotFoundError(SISError):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(SISError):
    """Raised when adding a student whose ID already exists."""


class StorageError(SISError):
    """Raised when reading/writing the data file fails."""
