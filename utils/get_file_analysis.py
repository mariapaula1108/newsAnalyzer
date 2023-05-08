import sqlite3

def get_file_analysis(email, file_name):
    # Connect to the user's database
    db_filename = f"{email}.db"
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    # Retrieve the file analysis data from the file_analysis table
    c.execute("SELECT file_content, keywords, sentiment, urls, topics FROM file_analysis WHERE file_name = ?", (file_name,))
    analysis_row = c.fetchone()

    if analysis_row is not None:
        file_content, keywords, sentiment, urls, topics = analysis_row
        file_content = file_content
        keywords = keywords.split(',')
        urls = urls.split(',')
        topics = topics.split(',')

        analysis_data = {
            'file_content' : file_content,
            'keywords': keywords,
            'sentiment': sentiment,
            'urls': urls,
            'topics': topics
            
        }
    else:
        analysis_data = None

    conn.close()
    return analysis_data
