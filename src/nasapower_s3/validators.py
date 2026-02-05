"""
Input validation utilities.
"""
from typing import Union

from .constants import FREQUENCIES, MAX_LAT, MAX_LON, MIN_LAT, MIN_LON
from .exceptions import InvalidCoordinateError, InvalidFrequencyError


def validate_coordinates(lat: float, lon: float) -> None:
    """
    Validate latitude and longitude.
    
    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        
    Raises:
        InvalidCoordinateError: If coordinates are out of bounds.
    """
    if not (MIN_LAT <= lat <= MAX_LAT):
        raise InvalidCoordinateError(
            f"Invalid Latitude: {lat}. Must be between {MIN_LAT} and {MAX_LAT}."
        )
    if not (MIN_LON <= lon <= MAX_LON):
        raise InvalidCoordinateError(
            f"Invalid Longitude: {lon}. Must be between {MIN_LON} and {MAX_LON}."
        )


def validate_frequency(frequency: str) -> None:
    """
    Validate data frequency.

    Args:
        frequency: Data frequency string (e.g., 'daily', 'hourly')

    Raises:
        InvalidFrequencyError: If frequency is not supported.
    """
    if frequency not in FREQUENCIES:
        raise InvalidFrequencyError(
            f"Invalid frequency: '{frequency}'. Supported values: {FREQUENCIES}"
        )
