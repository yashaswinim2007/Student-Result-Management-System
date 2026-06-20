import sqlite3
import os

def create_db():
    # Find the correct folder path
    current_folder = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_folder, "PIP.db")
    
    # 1. Establish the connection
    con = sqlite3.connect(database=db_path)
    
    # 2. Create the cursor (your tool for executing SQL commands)
    cur = con.cursor()
    
    # 3. Execute the command to create the table if it doesn't exist yet
    cur.execute("CREATE TABLE IF NOT EXISTS course (cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    
    # 4. Commit (save) the changes to the database
    con.commit()
    
    print("Database and 'course' table verified/created successfully!")
    
    # 5. Close the connection
    con.close()

create_db()

