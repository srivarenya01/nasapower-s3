"""
Tests for the nasapower-s3 library.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import numpy as np

from nasapower_s3 import NasaPowerS3
from nasapower_s3.validators import validate_coordinates, validate_frequency
from nasapower_s3.exceptions import (
    InvalidCoordinateError,
    InvalidFrequencyError,
    VariableNotFoundError,
    DataAccessError,
)


class TestValidators:
    """Test input validation functions."""

    def test_valid_coordinates(self):
        """Valid coordinates should not raise."""
        validate_coordinates(0, 0)
        validate_coordinates(90, 180)
        validate_coordinates(-90, -180)
        validate_coordinates(30.6, -96.3)

    def test_invalid_latitude(self):
        """Latitude out of range should raise InvalidCoordinateError."""
        with pytest.raises(InvalidCoordinateError):
            validate_coordinates(91, 0)
        with pytest.raises(InvalidCoordinateError):
            validate_coordinates(-91, 0)

    def test_invalid_longitude(self):
        """Longitude out of range should raise InvalidCoordinateError."""
        with pytest.raises(InvalidCoordinateError):
            validate_coordinates(0, 181)
        with pytest.raises(InvalidCoordinateError):
            validate_coordinates(0, -181)

    def test_valid_frequency(self):
        """Valid frequencies should not raise."""
        validate_frequency("daily")
        validate_frequency("hourly")
        validate_frequency("monthly")

    def test_invalid_frequency(self):
        """Invalid frequency should raise InvalidFrequencyError."""
        with pytest.raises(InvalidFrequencyError):
            validate_frequency("weekly")
        with pytest.raises(InvalidFrequencyError):
            validate_frequency("invalid")


class TestNasaPowerS3Client:
    """Test the main NasaPowerS3 client."""

    def test_client_initialization(self):
        """Client should initialize without errors."""
        client = NasaPowerS3()
        assert client is not None

    def test_invalid_collection(self):
        """Invalid collection should raise DataAccessError."""
        client = NasaPowerS3()
        with pytest.raises((ValueError, DataAccessError)):
            client.get_data(
                lat=30.6,
                lon=-96.3,
                start_date="2023-01-01",
                end_date="2023-01-10",
                variables=["T2M"],
                collection="invalid_collection",
            )

    @pytest.mark.integration
    def test_real_data_fetch(self):
        """Integration test: Fetch real data from S3."""
        client = NasaPowerS3()
        df = client.get_data(
            lat=30.6,
            lon=-96.3,
            start_date="2023-01-01",
            end_date="2023-01-05",
            variables=["T2M"],
            frequency="daily",
            collection="meteorology",
        )
        
        # Verify structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5  # 5 days
        assert "T2M" in df.columns
        assert "time" in df.columns
        assert "lat" in df.columns
        assert "lon" in df.columns
        
        # Verify data types
        assert df["T2M"].dtype in [np.float32, np.float64]


    def test_update_buckets_template(self):
        """Test updating a collection with a new template."""
        client = NasaPowerS3()
        new_template = "s3://new-bucket/power_{freq}.zarr"
        client.update_buckets("new_collection", url=new_template)
        
        # We can't easily fetch from a fake S3 URL without more mocking,
        # but we can verify the internal state.
        assert client._buckets["new_collection"] == new_template
        
    def test_update_buckets_override(self):
        """Test updating a specific frequency override."""
        client = NasaPowerS3()
        client.update_buckets("meteorology", frequency="daily", url="s3://custom-daily.zarr")
        
        assert isinstance(client._buckets["meteorology"], dict)
        assert client._buckets["meteorology"]["daily"] == "s3://custom-daily.zarr"

    def test_instance_isolation(self):
        """Test that updating one client doesn't affect another."""
        client1 = NasaPowerS3()
        client2 = NasaPowerS3()
        
        client1.update_buckets("meteorology", frequency="daily", url="s3://custom-daily.zarr")
        
        # client1 should be updated
        assert isinstance(client1._buckets["meteorology"], dict)
        # client2 should still have the default template string
        assert isinstance(client2._buckets["meteorology"], str)
        assert "{freq}" in client2._buckets["meteorology"]


class TestExceptions:
    """Test custom exception classes."""

    def test_invalid_coordinate_error(self):
        """InvalidCoordinateError should be raisable with message."""
        with pytest.raises(InvalidCoordinateError, match="test message"):
            raise InvalidCoordinateError("test message")

    def test_variable_not_found_error(self):
        """VariableNotFoundError should be raisable."""
        with pytest.raises(VariableNotFoundError):
            raise VariableNotFoundError("Variable XYZ not found")

    def test_data_access_error(self):
        """DataAccessError should be raisable."""
        with pytest.raises(DataAccessError):
            raise DataAccessError("S3 connection failed")
