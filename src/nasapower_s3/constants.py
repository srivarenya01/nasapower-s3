"""
Constants and mappings for NASA POWER S3 Zarr stores.
"""

# Zarr store URLs
# Zarr store URLs
# Structure matches S3: s3://nasa-power/{collection}/temporal/power_{collection}_{freq}_temporal_utc.zarr
BUCKETS = {
    "meteorology": "s3://nasa-power/merra2/temporal/power_merra2_{freq}_temporal_utc.zarr",
    "solar": "s3://nasa-power/srb/temporal/power_srb_{freq}_temporal_utc.zarr",
}

# Coordinate boundaries
MIN_LAT = -90.0
MAX_LAT = 90.0
MIN_LON = -180.0
MAX_LON = 180.0

# Supported frequencies
FREQUENCIES = ["daily", "hourly", "monthly", "climatology", "annual"]


# Common variables default collection map
# If a variable is in this list, we can guess the collection.
# Solar variables often start with ALLSKY, CLR, TOA, SZA
# Meteorology variables are often T2M, PRECTOT, RH, WS
VARIABLE_COLLECTION_MAP = {
    # Default Meteorology (MERRA-2)
    "T2M": "meteorology",
    "T2M_MAX": "meteorology",
    "T2M_MIN": "meteorology",
    "PRECTOTCORR": "meteorology",
    "RH2M": "meteorology",
    "WS10M": "meteorology",
    "PS": "meteorology",
    
    # Default Solar (SRB)
    "ALLSKY_SFC_SW_DWN": "solar",
    "CLR_SFC_SW_DWN": "solar",
    "ALLSKY_KT": "solar",
    "ALLSKY_SFC_LW_DWN": "solar",
    "TOA_SW_DWN": "solar",
}
