from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
import os
import boto3
import jwt  # Import JWT library
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64


# Secure JWT configuration
JWT_SECRET = "xxxxxxxxxxxxxxxxxxxxxx"  # Change this to a strong secret key
JWT_ALGORITHM = "HS256"

# Generate a secret key (store it securely!)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_file(file_data):
    return cipher.encrypt(file_data)

def decrypt_file(encrypted_data):
    return cipher.decrypt(encrypted_data)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure key for session management

oauth = OAuth(app)

oauth.register(
  name='oidc',
  client_id='xxxxxxxxxxxxxxxxxxx',
  client_secret='xxxxxxxxxxxxxxxxxxxxxx',
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_abvYIcCgM/.well-known/openid-configuration',
  client_kwargs={'scope': 'phone openid email'}
)

# Initialize S3 client
s3 = boto3.client('s3')
BUCKET_NAME = "cloud-file-storage-242"

# Adding a home page with links to login and logout routes.
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth-status')
def auth_status():
    user_email = get_current_user()
    return jsonify({"loggedIn": bool(user_email), "user": user_email})



# Configuring a login route to direct to Amazon Cognito managed login for authentication 
# with a redirect to an authorize route.        

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)


# The OAuth module collects the access token and retrieves user data from the Amazon Cognito
# userInfo endpoint. Configure an authorize route to handle the access token and user data 
# after authentication.


@app.route('/authorize')
def authorize():
    try:
        token = oauth.oidc.authorize_access_token()
        user = token.get('userinfo', {})

        # Generate a JWT token for the user
        jwt_payload = {
            "sub": user.get("sub"),
            "email": user.get("email"),
            "exp": datetime.utcnow() + timedelta(hours=2)  # Token expires in 2 hours
        }
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        session['jwt_token'] = jwt_token  # Store JWT in session
        return redirect(url_for('home'))
    except Exception as e:
        return f"OAuth Error: {str(e)}", 400

def get_current_user():
    token = session.get("jwt_token")
    if not token:
        return None

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        session['user_email'] = decoded_token["email"]  # Store email in session
        return decoded_token["email"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        session.pop("jwt_token", None)  # Remove expired/invalid token
        return None



# Using GET for logout to keep it simple
@app.route('/logout')
def logout():
    session.pop('jwt_token', None)  # Remove JWT token
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    user_email = get_current_user()
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    if file.content_length > 10 * 1024 * 1024:  # Limit file size to 10MB
        return jsonify({"error": "File size exceeds 10MB"}), 400

    encrypted_data = cipher.encrypt(file.read())  # Encrypt file content
    s3_key = f"{user_email}/{file.filename}.enc"  # Store with .enc extension

    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=encrypted_data)
        return jsonify({"message": "File uploaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['GET'])
def download_file():
    user_email = get_current_user()
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    file_name = request.args.get('file_name')
    if not file_name:
        return jsonify({"error": "File name is required"}), 400

    s3_key = f"{user_email}/{file_name}.enc"
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        encrypted_data = obj['Body'].read()
        decrypted_data = cipher.decrypt(encrypted_data)  # Decrypt file

        return decrypted_data  # Send decrypted file to user
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete', methods=['DELETE'])
def delete_file():
    user_email = get_current_user()
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    file_name = request.json.get('file_name')
    if not file_name:
        return jsonify({"error": "File name is required"}), 400

    s3_key = f"{user_email}/{file_name}.enc"
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        return jsonify({"message": "File deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    user_email = get_current_user()
    if not user_email:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{user_email}/")
        files = [obj['Key'].split('/')[-1] for obj in response.get('Contents', [])]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
