import sqlite3
from sqlite3 import Error
import datetime
import os

# Define the path to the database
path_root = os.path.dirname(os.path.abspath(__file__))
database_file_path = str(path_root) + "/myinventory.db"
print("HERE is the database file:", database_file_path)

# Create a connection to the database
def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return None

# Insert new item
def insert_data():
    name = input("Enter the name of the item: ")
    quantity = input("Enter the quantity: ")
    tags = input("Enter tags (comma-separated): ")
    location = input("Enter the item's location: ")
    changemade = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    try:
        sql = "INSERT INTO inventory (name, quantity, tags, location, changemade) VALUES (?, ?, ?, ?, ?)"
        conn.execute(sql, (name, quantity, tags, location, changemade))
        conn.commit()
        print("*** Data saved to database. ***")
    except Error as e:
        print("*** Insert error: ", e)
        pass

# View data
def view_data():
    try:
        cursor = conn.execute("SELECT id, name, quantity, tags, location, changemade FROM inventory")
        alldata = []
        alldata.append(["ID", "Name", "Quantity", "Tags", "Location", "Last Update"])
        for row in cursor:
            thisrow = []
            for x in range(6):
                thisrow.append(row[x])
            alldata.append(thisrow)
        return alldata
    except Error as e:
        print(e)
        pass

# Update item
def update_data():
    for row in view_data():
        thisrow = "  --> "
        for item in row:
            thisrow += str(item) + "  "
        print(thisrow)
    update_ID = input("Enter the ID of the item to edit: ")
    print('''
        1 = edit name
        2 = edit quantity
        3 = edit tags
        4 = edit location
    ''')
    feature = input("Enter which feature of the item you want to edit: ")
    update_value = input("Editing " + feature + ": enter the new value: ")

    if feature == "1":
        sql = "UPDATE inventory SET name = ? WHERE id = ?"
    elif feature == "2":
        sql = "UPDATE inventory SET quantity = ? WHERE id = ?"
    elif feature == "3":
        sql = "UPDATE inventory SET tags = ? WHERE id = ?"
    elif feature == "4":
        sql = "UPDATE inventory SET location = ? WHERE id = ?"
        
    try:
        conn.execute(sql, (update_value, update_ID))
        sql = "UPDATE inventory SET changemade = ? WHERE id = ?"
        changemade = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
        conn.execute(sql, (changemade, update_ID))
        conn.commit()
    except Error as e:
        print(e)
        pass

# Delete item
def delete_data():
    id_ = input("Enter the ID for the item to delete: ")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM inventory WHERE ID = ?", (id_,))
    delete_item = cursor.fetchall()
    confirm = input("Are you sure you want to delete " + id_ + " " + str(delete_item[0]) + "? (Enter 'y' to confirm.)")
    if confirm.lower() == "y":
        try:
            delete_sql = "DELETE FROM inventory WHERE id = ?"
            conn.execute(delete_sql, (id_,))
            conn.commit()
            print(id_ + " " + str(delete_item[0]) + " deleted.")
        except Error as e:
            print(e)
            pass
    else:
        print("Deletion aborted.")

# Initialize the database
def initialize_database():
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER DEFAULT 0,
            tags TEXT DEFAULT '',
            location TEXT DEFAULT '',
            changemade TEXT DEFAULT ''
        )
        """
        conn.execute(sql)
        conn.commit()
    except Error as e:
        print("*** Database Initialization Error: ", e)

# Main logic
conn = create_connection(database_file_path)
now = datetime.datetime.now()

if conn:
    print("Connected to database:", conn)
    initialize_database()
else:
    print("Error connecting to database.")
    exit()

while True:
    print("\nWelcome to the Inventory Management System!")
    print("1 to view data")
    print("2 to insert a new item")
    print("3 to update an item")
    print("4 to delete an item")
    print("X to exit")
    choice = input("Choose an operation to perform: ")
    if choice == "1":
        for row in view_data():
            thisrow = "  --> "
            for item in row:
                thisrow += str(item) + "  "
            print(thisrow)
    elif choice == "2":
        insert_data()
    elif choice == "3":
        update_data()
    elif choice == "4":
        delete_data()
    elif choice.upper() == "X":
        conn.close()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
