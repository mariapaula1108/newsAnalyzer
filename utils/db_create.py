import sqlite3
import os

def db_create(email):
    # Create a database file for the user
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    # Check if the files table already exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
    file_table_exists = c.fetchone() is not None

    # If the table does not exist, create it
    if not file_table_exists:
        c.execute('''CREATE TABLE files
                    (filename text, content blob)''')

    # Check if the keywords table already exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keywords'")
    key_table_exists = c.fetchone() is not None

    if not key_table_exists: 
        c.execute('''CREATE TABLE keywords
             (filename text, keyword text)''')

    # Insert the email into the users table
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    user_table_exists = c.fetchone() is not None

    if not user_table_exists:
        c.execute('''CREATE TABLE users
                    (email text)''')

    c.execute("INSERT INTO users VALUES (?)", (email,))
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_files'")
    user_files_table_exists = c.fetchone() is not None

    # If the table does not exist, create it
    if not user_files_table_exists:
        c.execute('''CREATE TABLE user_files
                    (id INTEGER PRIMARY KEY,
                     user_email text,
                     file_name text,
                     upload_time TIMESTAMP)''')
        
    # Check if the file_analysis table already exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_analysis'")
    file_analysis_table_exists = c.fetchone() is not None

    # If the table does not exist, create it
    if not file_analysis_table_exists:
        c.execute('''CREATE TABLE file_analysis
                    (file_name text, keywords text, sentiment text, urls text)''')
    
    conn.commit()

    conn.close()
    
    return f"Database created for user {email}"