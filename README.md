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

1. `app.py`: Contains the Flask application and API endpoints.
2. `keyword_extractor.py`: Extracts keywords from a given text.
3. `sentiment_extractor.py`: Analyzes the sentiment of a given text.
4. `search_web.py`: Searches the web for relevant URLs based on the provided keywords.
5. `db_create.py`: Creates a new SQLite database for a user identified by their email address.
6. `save_db.py`: Saves the analyzed PDF document's results to the user's database.
7. `search_db.py`: Searches the user's database for a keyword and returns a list of relevant file names.

### How to Run the Project

1. Ensure you have Python 3.6 or later installed on your system.
2. Install the required dependencies by running: `pip install -r requirements.txt`
3. Set the necessary environment variables (if required), such as API keys.
4. Run the Flask application with: `export FLASK_APP=app 
flask run`

