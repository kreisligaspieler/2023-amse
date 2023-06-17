import pandas as pd
from sqlalchemy import create_engine

#import data
engine = create_engine('sqlite:///./cars.sqlite')
df = pd.read_csv("https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv",sep=';', encoding='ISO-8859-1', skiprows=6, skipfooter=4, header=None, usecols=[0,1,2, 12, 22, 32, 42,52, 62,72],names=['date', 'CIN', 'name','petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others'], dtype={'date': str, 'CIN': str, 'name': str})
#dtype={'date': str, 'CIN': str, 'name': str,'petrol': int, 'diesel': int, 'gas': int, 'electro': int, 'hybrid': int, 'plugInHybrid': int, 'others': int},
#
#filter data
# CIN
patternDel = "^[0-9]{5}$/"
filter = df['CIN'].str.contains(patternDel, na=False)
df = df[~filter]
# convert to integer
df['petrol']=pd.to_numeric(df['petrol'], downcast='integer', errors='coerce')
df['diesel']=pd.to_numeric(df['diesel'], downcast='integer', errors='coerce')
df['gas']=pd.to_numeric(df['gas'], downcast='integer', errors='coerce')
df['electro']=pd.to_numeric(df['electro'], downcast='integer', errors='coerce')
df['hybrid']=pd.to_numeric(df['hybrid'], downcast='integer', errors='coerce')
df['plugInHybrid']=pd.to_numeric(df['plugInHybrid'], downcast='integer', errors='coerce')
df['others']=pd.to_numeric(df['others'], downcast='integer', errors='coerce')
# drop NaN
df=df.dropna()
df.to_sql("cars", con=engine, index=False)