# Azure OCR Documents

## Description

This project is a web application that allows users to upload documents (PDFs or images) and extract text from them using Azure Cognitive Services. The extracted text is then parsed and stored in a PostgreSQL database for future reference. The application also provides a download link for recent invoices in CSV format.

## Requirements

- Python
- Azure Cognitive Services (Document Intelligence)
- PostgreSQL
- Streamlit
- dotenv

## Setup

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/navi-0115/azure-ocr-streamlit.git
   ```

2. Create a new virtual environment and activate it.
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages using:

   ```
   pip install -r requirements.txt
   ```

4. Create a .env file in the root directory and add the following variables:

   ```
   AZURE_SERVICE_KEY=your_azure_service_key
   AZURE_SERVICE_REGION=your_azure_service_region
   AZURE_SERVICE_ENDPOINT=your_azure_service_endpoint
   AZURE_MODEL_ID=your_azure_model_id
   DATABASE_URL=your_postgresql_connection_string
   ```

5. Run the database migrations using Alembic:

   ```
   alembic upgrade head
   ```

6. Start the Streamlit application:
   ```
   streamlit run app.py
   ```
