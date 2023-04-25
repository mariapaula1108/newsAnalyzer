import os
import io
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests
from google.cloud import storage
import chardet
import PyPDF2
from keyword_extractor import extract_keywords
from sentiment_extractor import analyze_pdf_sentiment
from search_web import search_web
from save_db import save_db
from db_create import db_create

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
@app.route('/login')
def login():
    flow = Flow.from_client_config(
        OAUTH2_CLIENT_CONFIG,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    auth_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
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

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    idinfo = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), CLIENT_ID)

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    session['user_id'] = idinfo['sub']
    session['email'] = idinfo['email']
    session['name'] = idinfo.get('name', 'Unknown')
    
    email=session['email']
    
    create_request = db_create(email)
    print(create_request)
    
    return redirect(url_for('upload', email=email))



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

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
            
            # Upload the file to Google Cloud Storage
            bucket = storage_client.get_bucket(BUCKET_NAME)
            blob = bucket.blob(filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

            flash(f'File uploaded successfully: {filename}')
            flash(f'Keywords found successfully: {keyword_list}')
            flash(f'Sentiment analysis complete: {paragraph_sentiment}')
            flash(f'Here are some similar articles to the file uploaded: {urls}')

            return redirect(url_for('upload', email=session['email']))

    return render_template('upload.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
