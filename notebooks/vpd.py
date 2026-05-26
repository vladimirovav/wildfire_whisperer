import cdsapi
import xarray as xr
import numpy as np
import pandas as pd
import geopandas as gpd
import tempfile
import os

#I saved the polgyon locally so this just requests an input for the path

boundary_path = input("Path to boundary file (.shp or .json): ")
gdf = gpd.read_file(boundary_path).to_crs('EPSG:4326')
bounds = gdf.total_bounds  # west, south, east, north

# Download data from era5
c = cdsapi.Client()

tmp = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)
tmp_path = tmp.name
tmp.close()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': ['2m_temperature', '2m_dewpoint_temperature'],
        'year': '2023', #just a sample file so i'm only getting 2023 data
        'month': [f'{m:02d}' for m in range(1, 13)],
        'day': [f'{d:02d}' for d in range(1, 32)],
        'time': '12:00',
        'format': 'netcdf',
    },
    tmp_path
)

ds = xr.open_dataset(tmp_path, drop_variables=['expver', 'number']).load()
os.remove(tmp_path)

# Longitude comes 0-360, so we convert to -180-180
ds = ds.assign_coords(longitude=(ds.longitude % 360))
ds = ds.assign_coords(longitude=((ds.longitude + 180) % 360 - 180))
ds = ds.sortby('longitude')


ds = ds.sel(
    latitude=slice(bounds[3], bounds[1]),
    longitude=slice(bounds[0], bounds[2])
)

# VPD Calc using Buck equation. Here, among other places. This site only has the above 0C formula listed. The below 0C one uses slightly different constants https://www.omnicalculator.com/chemistry/vapour-pressure-of-water

T  = ds['t2m'] - 273.15
Td = ds['d2m'] - 273.15

# Buck equation changes below 0C so conditional calc based on temp value


# T >= 0°C


svp_liquid = 0.61121 * np.exp((18.678 - T / 234.5) * (T / (257.14 + T)))
avp_liquid = 0.61121 * np.exp((18.678 - Td / 234.5) * (Td / (257.14 + Td)))

# T < 0°C

svp_ice = 0.61115 * np.exp((23.036 - T / 333.7) * (T / (279.82 + T)))
avp_ice = 0.61115 * np.exp((23.036 - Td / 333.7) * (Td / (279.82 + Td)))

# Conditionally use formula based on Temp
svp = xr.where(T >= 0, svp_liquid, svp_ice)
avp = xr.where(T >= 0, avp_liquid, avp_ice)

vpd = (svp - avp).clip(min=0)
vpd.name = 'VPD_kPa'

# convert to df and drop null values + remove missing dates

df = vpd.to_dataframe().reset_index()
df = df.dropna()
df = df[df['VPD_kPa'] > 0]


df['valid_time'] = pd.to_datetime(df['valid_time'])
dates = df['valid_time'].dt.date.unique()
expected = pd.date_range('2023-01-01', '2023-12-31').date
missing = set(expected) - set(dates)

print('Days found:', len(dates))
print('Days expected:', len(expected))
if missing:
    print('Missing days:', sorted(missing))
else:
    print('No missing days!')

# Generate Shapefile
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs='EPSG:4326')
gdf.to_file('vpd.shp')
print('Final shape:', gdf.shape)
print('Saved to vpd.shp')
