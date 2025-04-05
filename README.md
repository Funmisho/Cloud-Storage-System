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
   * Set up AWS Cognito:
     - Go to the AWS Cognito Console and create a new user pool.
     - Configure user pool settings (make sure to enable email-based login or other methods depending on your use case).
   * Create an app client:
     - In the "App Clients" section, create a new app client
     - Ensure the "Enable sign-in API" option is checked.
   * 


   
  
