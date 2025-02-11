"""Downloads datasets and writes them into a sqlite-database. To get the database, install all requirements from requirements.txt and execute this file. Might also work with other versions of the required packages. 
Tested successfully with python3.10.6."""

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('sqlite:///../data/data.sqlite')
# read the data
df1 = pd.read_csv("https://data.bsh.de/OpenData/DOD/MO_H_CHLA/MO_H_CHLA_2018.txt",sep='\t',skiprows=103, encoding='ISO-8859-15', skip_blank_lines=True, header=0, names=["Cruise", "Station","Type", "Date", "Longitude [degrees_east]", "Latitude [degrees_north]", "LOCAL_CDI_ID","EDMO_code", "Bot Depth [m]", "Depth [m]", "QV_1", "CHLA_FLM_FGN_AL [µg/l]", "QV_2", "CHLA_SENE_DEV_NDT [µg/l]", "QV_3", " "],usecols=range(15), decimal=',')
df2 = pd.read_csv("https://data.bsh.de/OpenData/DOD/MO_H_CHLA/MO_H_CHLA_2022.txt",sep='\t',skiprows=91, encoding='ISO-8859-15', skip_blank_lines=True, header=0, names=["Cruise", "Station","Type", "Date", "Longitude [degrees_east]", "Latitude [degrees_north]", "LOCAL_CDI_ID","EDMO_code", "Bot Depth [m]", "Depth [m]", "QV_1", "CHLA_SENE_DEV_NDT [µg/l]", "QV_2", "CHLA_WAS_PTM_F_ACE [µg/l]", "QV3"],usecols=range(15), decimal=',')
df3 = pd.read_csv("https://data.bsh.de/OpenData/DOD/MO_H_TEMP/MO_H_TEMP_2018.txt",sep='\t',skiprows=103, encoding='ISO-8859-15', skip_blank_lines=True, header=0, names=["Cruise", "Station","Type", "Date", "Longitude [degrees_east]", "Latitude [degrees_north]", "LOCAL_CDI_ID","EDMO_code", "Bot Depth [m]", "Depth [m]", "QV_1", "TEMP_THE_NOT_NDT[°C]", "QV_2", "TEMP_THEPRC_NOT_NDT[°C]", "QV_3"],usecols=range(15), decimal=',')
df4 = pd.read_csv("https://data.bsh.de/OpenData/DOD/MO_H_TEMP/MO_H_TEMP_2022.txt",sep='\t',skiprows=91, encoding='ISO-8859-15', skip_blank_lines=True, header=0, names=["Cruise", "Station","Type", "Date", "Longitude [degrees_east]", "Latitude [degrees_north]", "LOCAL_CDI_ID","EDMO_code", "Bot Depth [m]", "Depth [m]", "QV_1", "TEMP_THE_NOT_NDT[°C]", "QV_2", "TEMP_SBE9_THEPRC_DEV_NDT", "QV3"],usecols=range(15), decimal=',') 

# save the data to slqite3
df1.to_sql("CHLA_18", con=engine, index=False)
df2.to_sql("CHLA_22", con=engine, index=False)
df3.to_sql("TEMP_18", con=engine, index=False)
df4.to_sql("TEMP_22", con=engine, index=False) 