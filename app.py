import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.structured_extraction import extract_text
from services.structured_parse import parse_invoice_data
from services.database_service import store_invoice_data, get_recent_invoices
from models.database_config import get_db_session  
from services.preprocess_image import preprocess_image
from services.insert_invoice_types import initialize_invoice_types
import os
from pdf2image import convert_from_bytes
from PIL import Image
import cv2
import numpy as np

# Load environment variables
load_dotenv()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Streamlit app
st.title("Invoice OCR and Data Extraction")

# Initialize hardcoded invoice types
initialize_invoice_types()

# Initialize session state
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set() 
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Upload multiple PDFs or images
uploaded_files = st.file_uploader(
    "Upload PDF or image invoices", 
    type=["pdf", "jpg", "jpeg", "png"], 
    accept_multiple_files=True,
    key="file_uploader"
)
# Reset session state if new files are uploaded
if uploaded_files and st.session_state.get("previous_files") != uploaded_files:
    st.session_state.processed = False
    st.session_state.previous_files = uploaded_files
    
# Prepare CSV download for last 30 days
db = get_db_session()
recent_invoices = get_recent_invoices(db, days=30)  
csv_path = os.path.join("outputs", "recent_invoices.csv")
recent_df = pd.DataFrame(recent_invoices) 

# Provide download link
csv_data = recent_df.to_csv(index=False, encoding="utf-8-sig")
st.download_button(
    label="Download Invoices (Last 30 Days)",
    data=csv_data.encode("utf-8-sig"),
    file_name="recent_invoices.csv",
    mime="text/csv",
)

if uploaded_files and not st.session_state.processed:
    try:
        all_parsed_data = []  # To store parsed data from all files

        for uploaded_file in uploaded_files:
            st.write(f"Processing file: {uploaded_file.name}")
            structured_data = None

            if uploaded_file.type == "application/pdf":
                # Save the uploaded PDF temporarily
                pdf_path = os.path.join("uploads", uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Convert PDF to images
                images = convert_from_bytes(uploaded_file.getvalue())

                # Process each page
                for i, image in enumerate(images):
                    image_path = os.path.join("uploads", f'page_{i + 1}.jpg')
                    image.save(image_path, 'JPEG')

                    # Preprocess the image
                    image_np = np.array(image)
                    preprocessed_image = preprocess_image(image_np)
                    preprocessed_image_path = image_path.replace('.jpg', '_preprocessed.jpg')
                    cv2.imwrite(preprocessed_image_path, preprocessed_image)

                    # Extract text from the preprocessed image
                    with open(preprocessed_image_path, "rb") as image_file:
                        page_data = extract_text(image_file)
                        if structured_data is None:
                            structured_data = page_data
                        else:
                            structured_data.update(page_data)

            elif uploaded_file.type in ["image/jpeg", "image/png"]:
                # Open the image
                image = Image.open(uploaded_file)

                # Preprocess the image
                image_np = np.array(image) 
                preprocessed_image = preprocess_image(image_np)
                preprocessed_image_path = os.path.join("uploads", f'preprocessed_{uploaded_file.name}')
                cv2.imwrite(preprocessed_image_path, preprocessed_image)

                # Extract text from the preprocessed image
                with open(preprocessed_image_path, "rb") as image_file:
                    structured_data = extract_text(image_file)

            else:
                st.error(f"Unsupported file format for {uploaded_file.name}. Please upload a PDF or image (JPEG/PNG).")
                continue

            # Parse the structured data
            if structured_data:
                parsed_data = parse_invoice_data(structured_data)
                st.write(f"Parsed Data for {uploaded_file.name}:")
                st.json(parsed_data)
                print(f"streamlit parsed data for {uploaded_file.name}:", parsed_data)

                # Store the parsed data in the database
                store_invoice_data(parsed_data)
                st.success(f"Data from {uploaded_file.name} stored in the database!")
                print(f"Data from {uploaded_file.name} stored in the database!")

                # Append parsed data to the list
                all_parsed_data.append(parsed_data)

        st.session_state.processed = True

    except Exception as e:
        st.error(f"An error occurred on streamlit app: {str(e)}")