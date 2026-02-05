import logging
from typing import Dict, List, Optional, Union

import fsspec
import pandas as pd
import xarray as xr

from .constants import BUCKETS as DEFAULT_BUCKETS
from .exceptions import DataAccessError, VariableNotFoundError
from .validators import validate_coordinates, validate_frequency

# Configure logging
logger = logging.getLogger(__name__)


class NasaPowerS3:
    """
    A secure, high-speed interface for NASA POWER data via AWS S3.
    """

    def __init__(self):
        """Initialize the NASA POWER S3 client."""
        # Create a local copy of buckets to avoid global state mutation
        self._buckets = DEFAULT_BUCKETS.copy()

    def update_buckets(
        self, collection: str, frequency: Optional[str] = None, url: Optional[str] = None
    ) -> None:
        """
        Update or add a BUCKET mapping for this client instance.

        Args:
            collection: Collection name (e.g., "meteorology", "solar")
            frequency: Optional specific frequency name (e.g., "daily"). 
                       If None, the url is treated as a template.
            url: Valid S3 Zarr store URL or template with {freq}
        """
        if frequency is None:
            # Treat url as a template for all frequencies in this collection
            self._buckets[collection] = url
        else:
            # Add/Update a specific frequency override
            if collection not in self._buckets or isinstance(self._buckets[collection], str):
                self._buckets[collection] = {}
            self._buckets[collection][frequency] = url
        
        logger.info(f"Updated bucket mapping for collection '{collection}'")

    def get_data(
        self,
        lat: float,
        lon: float,
        start_date: str,
        end_date: str,
        variables: List[str],
        frequency: str = "daily",
        collection: str = "meteorology",
    ) -> pd.DataFrame:
        """
        Fetch data from NASA POWER S3 Zarr store.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            start_date: Start date (YYYY-MM-DD or YYYY-MM-DDTHH:MM)
            end_date: End date (YYYY-MM-DD or YYYY-MM-DDTHH:MM)
            variables: List of variable names to fetch (e.g., ["T2M", "PRECTOTCORR"])
            frequency: Data frequency ("daily", "hourly", "monthly")
            collection: Data collection ("meteorology" or "solar"). Defaults to "meteorology".

        Returns:
            pd.DataFrame: DataFrame containing the requested data.

        Raises:
            InvalidCoordinateError: If coordinates are invalid.
            InvalidFrequencyError: If frequency is not supported.
            VariableNotFoundError: If a variable is not found.
            DataAccessError: If there is an error accessing S3.
        """
        # Validate inputs
        validate_coordinates(lat, lon)
        validate_frequency(frequency)

        ds = None
        try:
            # Get the URL/template for this collection
            bucket_info = self._buckets.get(collection)
            if not bucket_info:
                raise ValueError(
                    f"Invalid collection: '{collection}'. Supported: {list(self._buckets.keys())}"
                )
            
            # Resolve the URL
            if isinstance(bucket_info, str):
                # It's a template
                url = bucket_info.format(freq=frequency)
            elif isinstance(bucket_info, dict):
                # It's a dictionary of frequency-specific URLs
                url = bucket_info.get(frequency)
                if not url:
                    raise DataAccessError(
                        f"Frequency '{frequency}' is not mapped for collection '{collection}'."
                    )
            else:
                raise DataAccessError(f"Malformed bucket configuration for '{collection}'")

            logger.info(f"Connecting to NASA POWER S3: {url} (anonymous access)")
            store = fsspec.get_mapper(url, anon=True)
            ds = xr.open_zarr(store, consolidated=True)
            
            # Check if variables exist in dataset
            missing_vars = [v for v in variables if v not in ds.data_vars]
            if missing_vars:
                raise VariableNotFoundError(
                    f"Variables not found in {frequency} dataset: {missing_vars}"
                )

            logger.debug(f"Subsetting data for {lat}, {lon} from {start_date} to {end_date}")
            # Subset data - select nearest lat/lon first, then slice time
            subset = ds[variables].sel(
                lat=lat,
                lon=lon,
                method="nearest",
            ).sel(
                time=slice(start_date, end_date)
            )

            # Convert to Pandas
            df = subset.to_dataframe().reset_index()
            return df

        except (ValueError, VariableNotFoundError) as e:
            # Re-raise validation or specific business logic errors
            raise
        except Exception as e:
            # Distinguish between connection errors and processing errors
            err_str = str(e).lower()
            if "keyerror" in err_str or "404" in err_str or "nosuchkey" in err_str:
                msg = (f"Frequency '{frequency}' may not be available for collection '{collection}'. "
                       f"Attempted to access: {url if 'url' in locals() else 'Unknown'}")
                logger.error(msg)
                raise DataAccessError(msg) from e
            
            msg = f"Error accessing/processing NASA POWER S3 data: {e}"
            logger.error(msg)
            raise DataAccessError(msg) from e
        finally:
            if ds is not None:
                ds.close()
