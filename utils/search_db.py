
from utils.keyword_extractor import extract_keywords
from utils.sentiment_extractor import analyze_pdf_sentiment
from utils.search_web import search_web
from utils.save_db import save_db
from utils.db_create import db_create


import sqlite3

def search_db(search_term):
    conn = sqlite3.connect('uploaded_files.db')
    c = conn.cursor()

    c.execute("SELECT filename FROM keywords WHERE keyword LIKE ?", ('%' + search_term + '%',))
    results = [row[0] for row in c.fetchall()]

    conn.close()

    return results
