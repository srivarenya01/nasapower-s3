# nasapower-s3

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A universal, secure, and fast interface for accessing NASA POWER data directly from AWS S3 Zarr stores.

## Features

- **High Speed**: Access data directly from S3 using Zarr (cloud-optimized file format).
- **Universal**: Supports Daily, Hourly, and Monthly temporal scales.
- **Easy**: Returns standard pandas DataFrames.
- **Secure**: No AWS credentials required (anonymous access).

## Installation

```bash
pip install nasapower-s3
```

## Usage

```python
from nasapower_s3 import NasaPowerS3

# Initialize client
client = NasaPowerS3()

# Fetch data (Meteorology)
df = client.get_data(
    lat=30.6,
    lon=-96.3,
    start_date="2023-01-01",
    end_date="2023-01-10",
    variables=["T2M", "PRECTOTCORR"],
    frequency="daily",
    collection="meteorology"  # Default
)

# Fetch Solar data
df_solar = client.get_data(
    lat=30.6,
    lon=-96.3,
    start_date="2023-01-01",
    end_date="2023-01-10",
    variables=["ALLSKY_SFC_SW_DWN"],
    frequency="daily",
    collection="solar"
)

print(df.head())
```

## Available Data

The library supports:
- **Collections**: `meteorology` (MERRA-2) and `solar` (SRB)
- **Frequencies**: `daily`, `hourly`, `monthly`, `climatology`

For a full list of variables, refer to the [NASA POWER API Docs](https://power.larc.nasa.gov/docs/services/api/).

## Data License & Attribution

The code in this repository is licensed under **MIT**.
The data accessed from NASA POWER is licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

**Attribution**:
> "These data were obtained from the NASA Langley Research Center POWER Project funded through the NASA Earth Science Directorate Applied Science Program."

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
