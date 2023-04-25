from flask import Flask, redirect, request, url_for, jsonify, session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests

app = Flask(__name__)
app.secret_key = 'AIzaSyCOUh7bGoLNogsMiSoFsR2CQW4NpKAVBss'  # Replace with your own secret key

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
            'http://localhost:5000/oauth2callback'
        ]
    }
}

# Login route
@app.route('/login')
def login():
    flow = Flow.from_client_config(
        OAUTH2_CLIENT_CONFIG,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

# OAuth2 callback route
@app.route('/oauth2callback')
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
    session['name'] = idinfo['name']

    return redirect(url_for('profile'))

# Profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_info = {
        'user_id': session['user_id'],
        'email': session['email'],
        'name': session['name']
    }

    return jsonify(user_info)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

