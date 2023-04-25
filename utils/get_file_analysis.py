import sqlite3

def get_file_analysis(email, file_name):
    # Connect to the user's database
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    # Retrieve the file analysis data from the file_analysis table
    c.execute("SELECT keywords, sentiment, urls FROM file_analysis WHERE file_name = ?", (file_name,))
    analysis_row = c.fetchone()

    if analysis_row is not None:
        keywords, sentiment, urls = analysis_row
        keywords = keywords.split(',')
        urls = urls.split(',')

        analysis_data = {
            'keywords': keywords,
            'sentiment': sentiment,
            'urls': urls
        }
    else:
        analysis_data = None

    conn.close()
    return analysis_data
