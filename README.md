# Cloud-Based File Storage System

## Project Overview
This project is a cloud-based file storage system, similar to Dropbox or Google Drive, where users can upload, download and manage files stored in AWS S3. The system incorporates user authentication via AWS Cognito to ensure secure access to the files.

## Features
- **File Upload and Download**: Users can securely upload and download files securely with encryption.
- **Authentication with AWS Cognito**: Users authenticate through AWS Cognito using OAuth2.0 to ensure secure access to the system.
- **Secure Storage using AWS S3**: Files are securely stored in AWS S3 with encryption for additional protection.
- **File Management**: Ability to list, rename and delete stored files.
- **Web Interface**: A simple UI for users to interact with the system.
- **Scalability and Security**: Best practices for cloud security and IAM implemented.

## Optimizing Security
This project takes several steps to ensure data security, privacy, and controlled access:

- **Authentication & Authorization**:
  - Integrated **AWS Cognito** for user identity management.
  - Enforced **JWT validation** to ensure only authenticated users can access protected routes.
  - Plan to implement **Multi-Factor Authentication (MFA)** for extra account security.
  - Will enforce **strong password policies** at the Cognito user pool level.

- **Secure Data Transmission**:
  - Enabled **client-side encryption** before files are uploaded to S3 to ensure data confidentiality—Amazon cannot read user data.
  - HTTPS will be used for all communication once the application is fully deployed.

- **Secure API Endpoints**:
  - Endpoints are protected by validating **JWTs issued by Cognito**.
  - Unauthorized or unauthenticated requests are rejected.


## Tech Stack
- **Flask**: A lightweight Python web framework to build the application.
- **Cloud Provider**: AWS(S3, Cognito, IAM, Elastic Beanstalk)
- **Backend**: Python(Flask API) + Boto3(AWS SDK)
- **Frontend**: HTML/CSS/Javascript
- **Deployment**: AWS Elastic Beanstalk

## Installation

### Requirements:
- Python 3.12 or above
- AWS account with access to Cognito and S3
- AWS CLI configured

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/Funmisho/Cloud-Storage-System.git
   cd cloud-storage-system
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up AWS Cognito:
   * Create a new `user pool`:
     - Go to the AWS Cognito Console and create a new user pool.
     - Configure user pool settings (make sure to enable email-based login or other methods depending on your use case).
   * Create an `app client`:
     - In the "App Clients" section, create a new app client
     - Ensure the "Enable sign-in API" option is checked.
   * Update the `COGNITO_CLIENT_SECRET`:
     - After creating the app client, note the client ID and client secret for your Cognito app.
     - replace them in the code
4. Set up environment variables: <br>
   Safe security measure to not hardcode secret codes, better to store them in environment variables. Create a `.env` file in the root directory or set the variables directly in your environment. These variables are used in the app via Python's `os` library
   - Set `COGNITO_CLIENT_SECRET` and `JWT_SECRET` in your `.env` file or environment.
   - Set up an AWS S3 bucket (replace `YOUR_BUCKET_NAME` in the app):
     ```bash
     export BUCKET_NAME="YOUR_BUCKET_NAME"
     ```
5. Run the Flask application locally:
   ```bash
   python3 app.py
   ```
   The application will be running at http://localhost:5000.

##  Deployment

### Attempt with AWS Elastic Beanstalk:

   - **Elastic Beanstalk Setup**: Initially, I tried deploying the application to Elastic Beanstalk (EBS), but encountered issues with the redirect URI for Cognito requiring HTTPS, which EBS couldn’t easily support.
     * **What Worked**: The backend worked fine once deployed but failed to meet the redirect URL requirement for authentication.
     * **Challenges**: The key issue was that EBS requires an HTTPS URL for Cognito’s login redirect, while the default EBS URL uses HTTP. Configuring a custom domain or switching to a different service like API Gateway would be required to fix this.
    
## 🧠 Challenges & Learnings
- **Improved Python Skills**: Building this application helped improve core Python programming skills, especially around environment management, working with libraries like `boto3`, and handling authentication logic.
- **Frontend Implementation**: Writing the HTML, CSS, and JavaScript for the frontend was challenging, as it’s not my primary area of strength. I relied on various documentation, Stack Overflow, and AI tools to understand and implement the UI.
- **Security Awareness**: Gained deeper understanding of secure authentication, JWT handling, IAM roles, and client-side encryption to protect user data.
- **AWS Services**: Navigating AWS Cognito, S3, and deployment options like Elastic Beanstalk was a big learning curve but helped solidify my cloud skills.

    
       
     
   


   
  
