import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('my_database.db')
        print("Connected to the database.")
        print("Database exists.")
        conn.close()
    except sqlite3.Error as e:
        print("Database does not exist.")

def check_table_presence(table_name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def check_columns_presence(table_name, column_names):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    table_columns = cursor.fetchall()
    cursor.close()
    conn.close()
    existing_columns = [column[1] for column in table_columns]
    return all(column in existing_columns for column in column_names)

def test_case_1():
    table_name = "Location_Traffic_Signs"
    print("Test case 1:")
    print("Checks if the Location_Traffic_Signs table exists and if it has the required columns.")
    print("Required columns: 'timeSinceStartMs', 'type', 'longitude', 'latitude'")
    if check_table_presence(table_name):
        column_names = ["timeSinceStartMs", "type", "longitude", "latitude"]
        if check_columns_presence(table_name, column_names):
            print("Test case 1 passes.")
        else:
            print("Test case 1 failed. Missing columns in Location_Traffic_Signs table.")
    else:
        print("Test case 1 failed. Location_Traffic_Signs table does not exist.")

def test_case_2():
    table_name = "Location_Traffic_Accidents"
    print("Test case 2:")
    print("Checks if the Location_Traffic_Accidents table exists.")
    if check_table_presence(table_name):
        print("Test case 2 passes.")
    else:
        print("Test case 2 failed. Location_Traffic_Accidents table does not exist.")

def main():
    check_database()
    test_case_1()
    test_case_2()
    print("Automated testing done.")

if __name__ == '__main__':
    main()