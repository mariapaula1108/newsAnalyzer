import sqlite3

def search_files(email, search_query):
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    # Search for file names containing the search query
    c.execute("SELECT file_name, upload_time FROM user_files WHERE user_email=? AND file_name LIKE ?", (email, f"%{search_query}%"))
    files = c.fetchall()

    # TODO: Implement searching within file content

    conn.close()

    return files
