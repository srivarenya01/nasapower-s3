"""
Sample usage of the nasapower-s3 library.
"""
from nasapower_s3 import NasaPowerS3

# Initialize the client
client = NasaPowerS3()

# Fetch daily meteorology data for College Station, TX
print("Fetching daily temperature data for College Station, TX...")
print("Location: 30.6°N, 96.3°W")
print("Date range: Jan 1-10, 2023")
print("Variables: T2M (Temperature at 2m)")
print("-" * 50)

df = client.get_data(
    lat=30.6,
    lon=-96.3,
    start_date="2023-01-01",
    end_date="2023-01-10",
    variables=["T2M"],
    frequency="daily",
    collection="meteorology"
)

print("\nResults:")
print(df.to_string())
print(f"\nTotal rows: {len(df)}")
