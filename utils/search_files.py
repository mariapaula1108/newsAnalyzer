import sqlite3
import json
import re
from utils.sentences_keyword import sentences_keyword


def search_files(email, search_query):
    print(f"Search query: {search_query}")  # Debugging line
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    # Search for file names containing the search query
    c.execute("SELECT file_name, upload_time, file_content, sentiment FROM user_files WHERE user_email=?", (email,))
    files = c.fetchall()

    # Search within file content
    search_results = []
    for file_name, upload_time, file_content, sentiment in files:
        if search_query in file_content:
        # Find the paragraph containing the search query
            paragraphs = file_content.split('\n\n')  # Assuming paragraphs are separated by two newline characters
            for paragraph in paragraphs:
                keyword_sentences = sentences_keyword(paragraph, search_query)
                if keyword_sentences:
                    search_results.extend([(file_name, upload_time, sentence, sentiment, search_query) for sentence in keyword_sentences])

    conn.close()

    return search_results
