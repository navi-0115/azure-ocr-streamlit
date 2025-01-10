import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from services.text_extraction import extract_text
from services.data_parsing import parse_invoice_data
from services.database_service import store_invoice_data
import os

load_dotenv()

# Streamlit app
st.title("Invoice OCR with Azure Document Intelligence")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF invoice", type="pdf")
if uploaded_file is not None:
    # Save the file temporarily
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text using Azure Document Intelligence
    extracted_text = extract_text(file_path)
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