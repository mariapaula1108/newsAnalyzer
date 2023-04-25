import sqlite3
import os


def save_db(pdf_file_path, main_k, email):
    # Connect to the user's database
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

    # Insert the file and its contents into the database
    filename = os.path.basename(pdf_file_path)

    c.execute("SELECT * FROM files WHERE filename=?", (filename,))
    row = c.fetchone()
    if row is not None:
        msg = f"{filename} already exists in the database for user {email}"
    else: 
        with open(pdf_file_path, 'rb') as f:
            content = f.read()

        c.execute("INSERT INTO files (filename, content) VALUES (?, ?)", (filename, content))
        conn.commit()

        for keyword in main_k:
            c.execute("INSERT INTO keywords VALUES (?, ?)", (filename, keyword))
            conn.commit()

        msg = f"File '{filename}'s content and keywords uploaded and stored in the database for user {email}"

    c.execute("SELECT keyword FROM keywords WHERE filename=?", (filename,))
    rows = c.fetchall()

    # Print the keywords
    #for row in rows:
        #print(row[0])

    conn.close()

    return msg
