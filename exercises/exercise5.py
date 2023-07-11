import pandas as pd
from sqlalchemy import create_engine
import urllib.request
import zipfile

#import data
urllib.request.urlretrieve('https://gtfs.rhoenenergie-bus.de/GTFS.zip', 'GTFS.zip')
engine = create_engine('sqlite:///./gtfs.sqlite')
# Open the zip file
with zipfile.ZipFile('GTFS.zip', 'r') as zip_ref:
    # Read the 'stops.txt' file into a Pandas DataFrame
    with zip_ref.open('stops.txt') as file:
        df = pd.read_csv(file, sep=',', encoding='UTF-8', header=0, usecols=[0,2,4,5,6],names=["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"], dtype={"stop_id": int, "stop_name": str, "stop_lat": float, "stop_lon":float, "zone_id": int})

#filter data
index_names = df[ df['zone_id'] != 2001 ].index
df.drop(index_names, inplace = True)

#validate data
invalid_lat_mask = (df['stop_lat'] < -90) | (df['stop_lat'] > 90)
invalid_lon_mask = (df['stop_lon'] < -90) | (df['stop_lon'] > 90)
invalid_rows_mask = invalid_lat_mask | invalid_lon_mask
df_validated = df[~invalid_rows_mask]

# drop NaN
df=df.dropna()
df.to_sql("stops", con=engine, index=False)


