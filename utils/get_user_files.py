import sqlite3

def get_user_files(email):
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    c.execute("SELECT file_name, upload_time FROM user_files WHERE user_email=?", (email,))
    files = c.fetchall()

    conn.close()

    return files
