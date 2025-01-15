# Azure OCR Documents

## Description

This project is a tool that allows users to upload documents and extract text from them using Azure Document Intelligent. The extracted text is processed to identify key invoice data, such as invoice numbers, dates, and amounts etc. The data is then stored into a database using PostgreSQL for future reference.

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
