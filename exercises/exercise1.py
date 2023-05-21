import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./exercises/airports.sqlite')
df = pd.read_csv("https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv",sep=';') 
df.to_sql("airports", con=engine)