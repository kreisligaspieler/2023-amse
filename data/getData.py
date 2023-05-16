import pandas
import requests
from lxml import html
import sqlite3

url1 = 'https://data.bsh.de/OpenData/DOD/MO_H_CHLA/'
url2 = 'https://data.bsh.de/OpenData/DOD/MO_H_TEMP/'
# dynamicly download all available datasets
# get webpage
r1 = requests.get(url1, allow_redirects=True)
source1 = html.fromstring(r1.content)
r2 = requests.get(url2, allow_redirects=True)
source2 = html.fromstring(r2.content)
# extract links
links1 = source1.xpath('//a/@href')
links2 = source2.xpath('//a/@href')
# filter dataset links
datasets1= [x for x in links1 if x.startswith("MO")]
datasets2= [x for x in links2 if x.startswith("MO")]
# download each dataset and process it
relative_path = "/home/elias/git/2023-amse/data/"
for d in datasets1:
    # download dataset
    r = requests.get(url1+d, allow_redirects=True)
    open(relative_path+d, 'wb').write(r.content)
     # connect to database
    con = sqlite3.connect(relative_path+"database.sqlite")
    cur = con.cursor()
    # remove comments, fix format of date column 
    filename=d.removesuffix(".txt")
    file = open(relative_path+d,'r', encoding='ISO-8859-15')
    # create table, datasets
    cur.execute("CREATE TABLE IF NOT EXISTS "+ filename + " (Cruise VARCHAR(255), Station VARCHAR(255), Type VARCHAR(10), Date TEXT, [Longitude degrees_east] REAL, [Latitude degrees_north] REAL, LOCAL_CDI_ID VARCHAR(255), EDMO_code VARCHAR(10), [Bot Depth in m] FLOAT, [Depth in m] FLOAT, QV INTEGER, [CHLA_FLM_FGN_ALC in µg/l] FLOAT, QV_1 INTEGER, [CHLA_PTM_F_ACE in µg/l]	FLOAT, QV_2 INTEGER, [CHLA_SENE_DEV_NDT in µg/l] FLOAT, QV_3 INTEGER, [CHLA_SENE_NOT_NDT in  µg/l] FLOAT, QV_4 INTEGER)")
    for line in file.readlines():
        if not (line.startswith('//')) and not line.isspace() and not line.startswith("Cruise"):
            # replace T in date and write line to database
            date_old = line.split("\t")[3]
            date_new = date_old.replace("T"," ")
            line=line.replace(date_old,date_new)
            # prepare line for sql statement
            count = line.count("\t") - 1
            line=line.replace(",", ".").replace("\t", "','", count)
            # if last vales are empty or dataset < 2020 -> padd with empty entries
            while count < 18:
                line=line+"','"
                count+=1
            line="'"+line+"'"
            cur.execute("INSERT INTO "+ filename+" VALUES("+line+");")
            con.commit()
    cur.close()
    con.close()
    file.close()
    

   