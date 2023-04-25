import sqlite3
import json
from datetime import datetime

def save_file_info(email, file_name, keyword_list, sentiment, urls):
    # Connect to the user's database
    conn = sqlite3.connect(f"{email}.db")
    c = conn.cursor()

    # Save the file info into the file_analysis table
    c.execute("INSERT INTO file_analysis (file_name, keywords, sentiment, urls) VALUES (?, ?, ?, ?)",
              (file_name, json.dumps(keyword_list), json.dumps(sentiment), json.dumps(urls)))

    # Save the file info into the user_files table
    upload_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO user_files (user_email, file_name, upload_time) VALUES (?, ?, ?)",
              (email, file_name, upload_time))

    conn.commit()
    conn.close()
