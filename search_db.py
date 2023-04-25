
from keyword_extractor import extract_keywords
from sentiment_extractor import analyze_pdf_sentiment
from search_web import search_web
from save_db import save_db
from db_create import db_create


import sqlite3

def search_db(search_term):
    conn = sqlite3.connect('uploaded_files.db')
    c = conn.cursor()

    c.execute("SELECT filename FROM keywords WHERE keyword LIKE ?", ('%' + search_term + '%',))
    results = [row[0] for row in c.fetchall()]

    conn.close()

    return results
