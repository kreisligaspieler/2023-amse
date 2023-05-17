"""Downloads datasets and writes them into a sqlite-database. All datasets containing chlorophyll a measurements are stored in one table.
The datasets containing temperature measurements are stored in a separate table. To get the database, install all requirements from requirements.txt and execute this file. 
Tested successfully with python3. 10.6."""
import requests
import sqlite3
import os

def download_and_process(url, statement, type):
    relative_path = "/home/elias/git/2023-amse/data/"
    # download dataset
    r = requests.get(url, allow_redirects=True)
    open(relative_path+type, 'wb').write(r.content)
    # connect to database
    con = sqlite3.connect(relative_path+"database.sqlite")
    cur = con.cursor()
    file = open(relative_path+type,'r', encoding='ISO-8859-15')
    # create table
    cur.execute(statement)
    for line in file.readlines():
        if not (line.startswith('//')) and not line.isspace() and not line.startswith("Cruise"): # skip comments, empty lines and heading
            # replace T in date and write line to database
            date_old = line.split("\t")[3]
            date_new = date_old.replace("T"," ")
            line=line.replace(date_old,date_new)
            # prepare line for sql statement
            count = line.count("\t") - 1
            line=line.replace(",", ".").replace("\t", "','", count)
            if(type=="CHLA"):
                # if last vales are empty or dataset = 2018 -> padd with empty entries
                while count < 18:
                    line=line+"','"
                    count+=1
                line="'"+line+"'"
            else: 
                # if last vales are empty -> padd with empty entries
                while count < 14:
                    line=line+"','"
                    count+=1
                line="'"+line+"'"
            # insert line into database
            cur.execute("INSERT INTO "+ type + " VALUES("+line+");")
            con.commit()
    cur.close()
    con.close()
    file.close()
    # cleanup 
    os.remove(relative_path+type)
    

url1 = 'https://data.bsh.de/OpenData/DOD/MO_H_CHLA/MO_H_CHLA_2018.txt'
url2 = 'https://data.bsh.de/OpenData/DOD/MO_H_CHLA/MO_H_CHLA_2022.txt'
url3 = 'https://data.bsh.de/OpenData/DOD/MO_H_TEMP/MO_H_TEMP_2018.txt'
url4 = 'https://data.bsh.de/OpenData/DOD/MO_H_TEMP/MO_H_TEMP_2022.txt'
# download CHLA-datasets and process them
# input-params: url of dataset, sql statement for generating table, type of dataset (CHLA or temp)  
statement_CHLA="CREATE TABLE IF NOT EXISTS CHLA (Cruise VARCHAR(255), Station VARCHAR(255), Type VARCHAR(10), Date TEXT, [Longitude degrees_east] REAL, [Latitude degrees_north] REAL, LOCAL_CDI_ID VARCHAR(255), EDMO_code VARCHAR(10), [Bot Depth in m] FLOAT, [Depth in m] FLOAT, QV INTEGER, [CHLA_FLM_FGN_ALC in µg/l] FLOAT, QV_1 INTEGER, [CHLA_PTM_F_ACE in µg/l]	FLOAT, QV_2 INTEGER, [CHLA_SENE_DEV_NDT in µg/l] FLOAT, QV_3 INTEGER, [CHLA_SENE_NOT_NDT in  µg/l] FLOAT, QV_4 INTEGER)"
statement_TEMP="CREATE TABLE IF NOT EXISTS TEMP (Cruise VARCHAR(255), Station VARCHAR(255), Type VARCHAR(10), Date TEXT, [Longitude degrees_east] REAL, [Latitude degrees_north] REAL, LOCAL_CDI_ID VARCHAR(255), EDMO_code VARCHAR(10), [Bot Depth in m] FLOAT, [Depth in m] FLOAT, QV INTEGER, [CHLA_FLM_FGN_ALC in µg/l] FLOAT, QV_1 INTEGER, [TEMP_THEPRC_DEV_NDT in °C]	FLOAT, QV_2 INTEGER)"
# parallelize it
download_and_process(url1, statement_CHLA, "CHLA")
download_and_process(url2, statement_CHLA, "CHLA")
download_and_process(url3, statement_TEMP, "TEMP")
download_and_process(url4, statement_TEMP, "TEMP")


    

   