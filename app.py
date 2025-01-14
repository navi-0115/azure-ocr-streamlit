import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.structured_extraction import extract_text
from services.structured_parse import parse_invoice_data
from services.database_service import store_invoice_data, get_recent_invoices
from models.database_config import get_db_session  
from services.preprocess_image import preprocess_image
import os
from pdf2image import convert_from_path
from PIL import Image
import cv2

# Load environment variables
load_dotenv()

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Streamlit app
st.title("Invoice OCR and Data Extraction")

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF invoice", type=["pdf"])

# Prepare CSV download for last 30 days
db = get_db_session()
recent_invoices = get_recent_invoices(db, days=30)  
csv_path = os.path.join("outputs", "recent_invoices.csv")
recent_df = pd.DataFrame(recent_invoices) 

# Provide download link
csv_data=recent_df.to_csv(index=False, encoding="utf-8-sig")
st.download_button(
    label="Download Invoices (Last 30 Days)",
    data=csv_data.encode("utf-8-sig"),
    file_name="recent_invoices.csv",
    mime="text/csv",
)

if uploaded_file is not None and not st.session_state.processed:
    try:
        
        if uploaded_file.type == "application/pdf":
            # process the pdf file
            images = convert_from_path(uploaded_file.name)
            
            for i, page in enumerate(images):
                image_path = os.path.join("uploads", f'page_{i + 1}.jpg')
                page.save(image_path, 'JPEG')
                image = cv2.imread(image_path)
                preprocessed_image = preprocess_image(image)
                preprocessed_image_path = image_path.replace('.jpg', '_preprocessed.jpg')
                cv2.imwrite(preprocessed_image_path, preprocessed_image)
                
                with open(preprocessed_image_path, "rb") as image_file:
                    structured_data = extract_text(image_file)
                
                
        elif uploaded_file.type == ["image/jpeg", "image/png"]:
            image = Image.open(uploaded_file)
            preprocessed_image = preprocess_image(image)
            preprocessed_image_path = uploaded_file.name.replace('.jpg', '_preprocessed.jpg').replace('.jpeg', '_preprocessed.jpeg').replace('.png', '_preprocessed.png')
            cv2.imwrite(preprocessed_image_path, preprocessed_image)
            
            with open(preprocessed_image_path, "rb") as image_file:
                structured_data = extract_text(image_file)
        else:
            st.error("Unsupported file format.")
            st.stop()

        # Parse the structured data
        parsed_data = parse_invoice_data(structured_data)
        st.write("Parsed Data:")
        st.json(parsed_data)
        print("streamlit parsed data:", parsed_data)

        # Store the parsed data in the database
        store_invoice_data(parsed_data)
        st.success("Data stored in the database!")
        print("Data stored in the database!")

        # # Display parsed data as a table
        # invoice_df = pd.DataFrame(parsed_data["invoice_items"])
        # invoice_df["invoice_number"] = parsed_data.get("invoice_number")
        # st.write("Invoice Items Table:")
        # st.dataframe(invoice_df)
        
        st.session_state.processed = True

    except Exception as e:
        st.error(f"An error occurred on streamlit app: {str(e)}")
