import sqlite3
import json
from datetime import datetime

def save_file_info(email, file_name, file_content, keyword_list, sentiment, urls, topics):
    # Connect to the user's database
    conn = sqlite3.connect(f"{email}.db")
    c = conn.cursor()

    # Save the file info into the file_analysis table
    c.execute("INSERT INTO file_analysis (file_name, file_content, keywords, sentiment, urls, topics) VALUES (?, ?, ?, ?, ?, ?)",
              (file_name, json.dumps(file_name), json.dumps(keyword_list), json.dumps(sentiment), json.dumps(urls), json.dumps(topics)))

    # Save the file info into the user_files table
    upload_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO user_files (user_email, file_name, upload_time) VALUES (?, ?, ?)",
              (email, file_name, upload_time))
    
    c.execute("UPDATE user_files SET file_content=?, sentiment=? WHERE user_email=? AND file_name=?", (file_content, json.dumps(sentiment), email, file_name))


    conn.commit()
    conn.close()
