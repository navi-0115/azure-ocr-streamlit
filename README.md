# Azure OCR Documents

## Description

This project is a web application that allows users to upload documents and extract text from them using Azure Cognitive Services. The extracted text is then stored in a database for future reference.

## Requirements

- Python 3.9
- Azure Cognitive Services
- SQL Server
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Script
- Flask-Cors

## Setup

1. Clone the repository to your local machine.
2. Create a new virtual environment and activate it.
3. Install the required packages using pip install -r requirements.txt.
4. Create a .env file in the root directory and add the following variables:
   - COG_SERVICE_KEY: Your Azure Cognitive Services key
   - COG_SERVICE_ENDPOINT: Your Azure Cognitive Services endpoint
   - DATABASE_URL: Your SQL Server connection string
5. Run the flask app using flask run or gunicorn.
