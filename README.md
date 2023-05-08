# newsAnalyzer
## app.py

`app.py` is the main entry point for your NewsAnalyzer application. This file contains the necessary endpoints for interacting with the application through APIs. It handles the incoming requests and provides appropriate responses by interacting with the underlying modules and functions.

### APIs

The following APIs are available in the NewsAnalyzer application:

1. **Create a User Database**: Creates a new SQLite database for a user identified by their email address.
   - Endpoint: `/db/create`
   - Method: `POST`
   - Payload: `{"email": "<user_email>"}`

2. **Analyze a PDF Document**: Analyzes a PDF document and extracts keywords, sentiment, and related URLs.
   - Endpoint: `/analyze`
   - Method: `POST`
   - Payload: `{"pdf_content": "<pdf_content>"}`

3. **Save File Analysis**: Saves the analyzed PDF document's results to the user's database.
   - Endpoint: `/save`
   - Method: `POST`
   - Payload: `{"email": "<user_email>", "file_name": "<file_name>", "file_content": "<file_content>", "sentiment": "<sentiment>", "keywords": "<keywords>", "urls": "<urls>", "topics": "<topics>"}`

4. **Search Database**: Searches the user's database for a keyword and returns a list of relevant file names.
   - Endpoint: `/search`
   - Method: `GET`
   - URL parameters: `email=<user_email>&search_term=<search_term>`

### Architecture

The NewsAnalyzer application consists of the following modules:

Architecture
The NewsAnalyzer application consists of the following modules:

1. app.py: Contains the Flask application and API endpoints.
2. keyword_extractor.py: Extracts keywords from a given text.
3. sentiment_extractor.py: Analyzes the sentiment of a given text.
4. search_web.py: Searches the web for relevant URLs based on the provided keywords.
5. db_create.py: Creates a new SQLite database for a user identified by their email address.
6. save_db.py: Saves the analyzed PDF document's results to the user's database.
7. search_db.py: Searches the user's database for a keyword and returns a list of relevant file names.
8. save_file_info.py: Saves the file information (e.g., keywords, sentiment, related URLs) to the user's database.
9. get_user_files.py: Retrieves the list of files uploaded by the user.
10. get_file_analysis.py: Retrieves the analysis data (keywords, sentiment, related URLs) for a specified file.
11. search_files.py: Searches the user's files based on the provided search term.
12. topic_extractor.py: Extracts topics from a given text.
13. extract_entities.py: Extracts entities from a given text.

### Additional Utilities
1. Google OAuth2: The application uses Google OAuth2 for user authentication, allowing users to log in with their Google accounts.
2. Google Cloud Storage: Uploaded files are stored in Google Cloud Storage, providing a scalable and secure solution for file storage.
3. PyPDF2: This library is used to extract text from PDF files, which is then used for analysis.
4. chardet: This library is used to detect the encoding of the uploaded files, ensuring correct handling of text data.
**Allowed Extensions:** The application restricts the types of files that can be uploaded. The allowed file types are txt, pdf, png, jpg, jpeg, and gif.

### How to Run the Project

1. Ensure you have Python 3.6 or later installed on your system.
2. Install the required dependencies by running: `pip install -r requirements.txt`
3. Run the following commands: `pip install --upgrade google-cloud-storage`
`python3 -m pip install scikit-learn`
`python -m spacy download en_core_web_sm`
4. Set the necessary environment variables (if required), such as API keys.
5. Run the Flask application with: `export FLASK_APP=app' 
'flask run`

