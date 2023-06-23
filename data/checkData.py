import sqlite3

def checkRows(table, numRows):
    con = sqlite3.connect("../data/data.sqlite")
    cur = con.cursor()
    rows = cur.execute("SELECT COUNT(*) FROM "+table)
    # Tables from 22 still got updated at the creation of the report
    if table == "TEMP_22" or table == "CHLA_22":
        if rows.fetchone() < (numRows,):
            print(table+": Not all rows hav been imported into database!")
            return False
    elif not rows.fetchone() == (numRows,):
        print(table+": Not all rows hav been imported into database!")
        return False
    return True
        
if checkRows("CHLA_18", 466) and checkRows("CHLA_22", 82938) and checkRows("TEMP_18", 50574) and checkRows("TEMP_22",144628):
    print("Data successfully imported into database.")
else:
    raise Exception("Data not successfully imported!")


