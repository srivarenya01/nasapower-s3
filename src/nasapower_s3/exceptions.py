class NasaPowerError(Exception):
    """Base exception for NASA POWER library."""
    pass


class InvalidCoordinateError(NasaPowerError):
    """Raised when coordinates are out of valid range."""
    pass


class InvalidFrequencyError(NasaPowerError):
    """Raised when an invalid frequency is requested."""
    pass


class VariableNotFoundError(NasaPowerError):
    """Raised when a requested variable is not found in the dataset."""
    pass


class DataAccessError(NasaPowerError):
    """Raised when there is an issue accessing the data source."""
    pass
