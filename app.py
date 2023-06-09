import os
import io
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from werkzeug.utils import secure_filename
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests
from google.cloud import storage
import chardet
import PyPDF2
from utils.keyword_extractor import extract_keywords
from utils.sentiment_extractor import analyze_pdf_sentiment
from utils.search_web import search_web
from utils.save_db import save_db
from utils.db_create import db_create
from utils.save_file_info import save_file_info
from utils.get_user_files import get_user_files
from utils.get_file_analysis import get_file_analysis
from utils.search_files import search_files
from utils.topic_extractor import extract_topics
from utils.extract_entities import extract_entities


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.secret_key = 'AIzaSyCOUh7bGoLNogsMiSoFsR2CQW4NpKAVBss'  # Replace with your own secret key


# Replace with your Google Cloud Storage bucket name
BUCKET_NAME = "bucket-quickstart_ec530-final-project-384115"

# Replace with your OAuth 2.0 credentials
CLIENT_ID = '967503734681-b3s7vggbemogqvg5g2knbqqufgjvu2pd.apps.googleusercontent.com'
CLIENT_SECRET = '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'


# Replace with your own client ID and secret
OAUTH2_CLIENT_CONFIG = {
    'web': {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://accounts.google.com/o/oauth2/token',
        'redirect_uris': [
            'http://localhost:5000/callback'
        ]
    }
}

# Google Cloud Storage client
storage_client = storage.Client.from_service_account_json('./ec530-final-project-384115-9b7b441d7031.json')

# Initialize the allowed extensions for file uploads
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login route
# Login route
@app.route('/login')
def login():
    # Initialize the OAuth2 flow
    flow = Flow.from_client_config(
        OAUTH2_CLIENT_CONFIG,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    # Get the authorization URL
    auth_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    session['user_name'] = None  # Initialize user name to None
    return redirect(auth_url)

# OAuth2 callback route
@app.route('/callback')
def oauth2callback():
    flow = Flow.from_client_config(
        OAUTH2_CLIENT_CONFIG,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=url_for('oauth2callback', _external=True),
        state=session['state']
    )

    # Fetch token
    flow.fetch_token(authorization_response=request.url)

    # Store credentials in the session
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    # Verify ID token
    idinfo = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), CLIENT_ID)
    
    # Validate the issuer
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    # Store user information in the session
    session['user_id'] = idinfo['sub']
    session['email'] = idinfo['email']
    session['name'] = idinfo.get('name', 'Unknown')
    
    email=session['email']
    
    # Create a new user database if it does not exist
    create_request = db_create(email)
    print(create_request)
    
    return redirect(url_for('upload', email=email))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user files
    email = session['email']
    user_files = get_user_files(email)
    name = session.get('name', 'Unknown')

    # Handle file uploads
    if request.method == 'POST':
        # Check if files were uploaded
        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files')

        # If the user does not select any file, the browser submits an empty list
        if not files or all(file.filename == '' for file in files):
            flash('No selected files')
            return redirect(request.url)

        user_files = get_user_files(email)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Check if the filename already exists in the user's files
                if filename in [file_name for file_name, _ in user_files]:
                    flash(f'File with the same name already exists: {filename}')
                    continue
                
                # Save the file without analyzing it if it's a PNG or JPG
                if file.content_type.startswith('image/'):
                    # Upload the file to Google Cloud Storage
                    bucket = storage_client.get_bucket(BUCKET_NAME)
                    blob = bucket.blob(filename)
                    file.seek(0)  # Add this line to reset the file read pointer
                    blob.upload_from_string(
                        file.read(),
                        content_type=file.content_type
                    )
                    save_file_info(email, filename, keyword_list=None, sentiment=None, urls=None, topics=None)
                
                # Otherwise, analyze the file
                else:
                    # Check if the file is a PDF file
                    if file.content_type == 'application/pdf':
                        # Extract text from PDF file
                        pdf_reader = PyPDF2.PdfReader(file)
                        file_content = ''
                        for page_num in range(len(pdf_reader.pages)):
                            page_obj = pdf_reader.pages[page_num]
                            file_content += page_obj.extract_text()

                    else:
                        # Detect the encoding of the file
                        file_content = io.BytesIO(file.read())
                        file_encoding = chardet.detect(file_content.read())['encoding']
                        if file_encoding is None or file_encoding == '':
                            file_encoding = 'utf-8'
                        file_content.seek(0)
                        file_content = file_content.read().decode(file_encoding, errors='ignore')

                    # Extract keywords from file content
                    keyword_list = extract_keywords(file_content)

                    # Analyze sentiment and extract keywords from file content
                    paragraph_sentiment = analyze_pdf_sentiment(file_content)
                    
                    # Search the web for similar articles 
                    urls = search_web(keyword_list)
                    
                    topics = extract_topics(file_content)
                    
                    save_file_info(email, filename, file_content, keyword_list, paragraph_sentiment, urls, topics)
                    
                    # Upload the file to Google Cloud Storage
                    bucket = storage_client.get_bucket(BUCKET_NAME)
                    blob = bucket.blob(filename)
                    file.seek(0)  # Add this line to reset the file read pointer
                    blob.upload_from_string(
                        file.read(),
                        content_type=file.content_type
                    )

                
    user_files = get_user_files(email) 
    return render_template('upload.html', files=user_files, email=session['email'], name=name)


@app.route('/files/<filename>')
def serve_file(filename):
    # Read the file content from Google Cloud Storage
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    file_content = blob.download_as_bytes()

    # Return the file content as a response with the appropriate content type
    response = Response(file_content, content_type=blob.content_type)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response


@app.route('/analysis/<filename>')
def analysis(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve the file analysis (keywords, sentiment, related articles) from the database
    analysis_data = get_file_analysis(session['email'], filename)
    
    # Retrieve the file content from the database
    file_content = analysis_data["file_content"]

    # Extract entities from the file content
    entities = extract_entities(file_content)

    # Add the entities to the analysis_data dictionary
    analysis_data["entities"] = entities

    return render_template('analysis.html', filename=filename, analysis_data=analysis_data)


@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        search_query = request.form['search_query']
        email = session['email']
        search_results = search_files(email, search_query)
        return render_template('search_results.html', search_results=search_results)
    return render_template('search.html')


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)



