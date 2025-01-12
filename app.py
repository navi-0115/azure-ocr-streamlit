import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from services.text_extraction import extract_text
from services.data_parsing import parse_invoice_data
from services.database_service import store_invoice_data
import os

# Load environment variables
load_dotenv()

# Create uploads and outputs directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Streamlit app
st.title("Invoice OCR and Data Extraction")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF invoice", type="pdf")
if uploaded_file is not None:
    try:
        # Extract text using Azure OCR
        extracted_text = extract_text(uploaded_file)
        st.write("Extracted Text:")
        st.text(extracted_text)

        # Parse extracted text into structured data
        parsed_data = parse_invoice_data(extracted_text)
        st.write("Parsed Data:")
        st.json(parsed_data)

        # Store the parsed data in the database
        store_invoice_data(parsed_data)
        st.success("Data stored in the database!")

        # Convert parsed data to CSV
        csv_path = os.path.join("outputs", "extracted_invoice.csv")
        df = pd.DataFrame([parsed_data])
        df.to_csv(csv_path, index=False)

        # Provide download link
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="extracted_invoice.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")