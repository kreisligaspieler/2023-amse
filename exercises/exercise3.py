import pandas as pd
from sqlalchemy import create_engine

#import data
engine = create_engine('sqlite:///./cars.sqlite')
df = pd.read_csv("https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv",sep=';', encoding='ISO-8859-1', skiprows=6, skipfooter=4, header=None, usecols=[0,1,2, 12, 22, 32, 42,52, 62,72],names=['date', 'CIN', 'name','petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others'], dtype={'date': str, 'CIN': str, 'name': str})

#filter data
# CIN
patternDel = "^[0-9]{5}$/"
filter = df['CIN'].str.contains(patternDel, na=False)
df = df[~filter]

# convert to integer
df['petrol']=pd.to_numeric(df['petrol'], errors='coerce').convert_dtypes(convert_integer=True)
df['diesel']=pd.to_numeric(df['diesel'], errors='coerce').convert_dtypes(convert_integer=True)
df['gas']=pd.to_numeric(df['gas'], errors='coerce').convert_dtypes(convert_integer=True)
df['electro']=pd.to_numeric(df['electro'], errors='coerce').convert_dtypes(convert_integer=True)
df['hybrid']=pd.to_numeric(df['hybrid'], errors='coerce').convert_dtypes(convert_integer=True)
df['plugInHybrid']=pd.to_numeric(df['plugInHybrid'], errors='coerce').convert_dtypes(convert_integer=True)
df['others']=pd.to_numeric(df['others'], errors='coerce').convert_dtypes(convert_integer=True)

# drop NaN
df=df.dropna()
df.to_sql("cars", con=engine, index=False)