import PyPDF2
from keyword_extractor import extract_keywords
from sentiment_extractor import analyze_pdf_sentiment
from search_web import search_web
from save_db import save_db
from db_create import db_create
import queue
import PyPDF2


def process_pdfs(pdf_files):
    # Create queue 
    pdf_queue = queue.Queue()

    # Upload files to queue
    for pdf_file in pdf_files:
        pdf_queue.put(pdf_file)

    # Process PDFs 
    all_done = False
    while not all_done:
        try:
            # Get next PDF 
            pdf_file = pdf_queue.get(timeout=1)  # add a timeout to avoid blocking indefinitely

            # Analyze PDF
            if pdf_file.content_type == 'application/pdf':
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                file_content = ''
                for page_num in range(len(pdf_reader.pages)):
                    page_obj = pdf_reader.pages[page_num]
                    file_content += page_obj.extract_text()

                keyword_list = extract_keywords(file_content)
                paragraph_sentiment = analyze_pdf_sentiment(file_content)
                urls = search_web(keyword_list)

                save_db(pdf_file.filename, pdf_file.read(), keyword_list, paragraph_sentiment, urls)

            # Mark PDF as processed
            pdf_queue.task_done()

        except queue.Empty:
            # If queue empty, exit the loop 
            all_done = True
            
            #hello 
