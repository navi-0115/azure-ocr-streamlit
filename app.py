import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.structured_extraction import extract_text
from services.structured_parse import parse_invoice_data
from services.database_service import store_invoice_data, get_recent_invoices
from models.database_config import get_db_session  
import os

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
uploaded_file = st.file_uploader("Upload a PDF invoice", type=["pdf", "jpg", "png"])
if uploaded_file is not None and not st.session_state.processed:
    try:
        # Extract text using Azure OCR
        structured_data = extract_text(uploaded_file)
        # st.write("Structured Data:")
        # st.json(structured_data)
        print("streamlit structured data:", structured_data)

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

        # Prepare CSV download for last 30 days
        db = get_db_session()
        recent_invoices = get_recent_invoices(db, days=30)  
        csv_path = os.path.join("outputs", "recent_invoices.csv")
        recent_df = pd.DataFrame(recent_invoices) 

        # Provide download link
        csv_data=recent_df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="Download Recent Invoices (Last 30 Days)",
            data=csv_data.encode("utf-8-sig"),
            file_name="recent_invoices.csv",
            mime="text/csv",
)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display the invoices stored in the last 30 days
# st.write("Invoices from the last 30 days:")
# db = get_db_session() 
# recent_invoices = get_recent_invoices(db, days=30)  
# if recent_invoices:
#     st.dataframe(pd.DataFrame(recent_invoices))
# else:
#     st.write("No invoices found in the last 30 days.")



# import streamlit as st
# import pandas as pd
# from dotenv import load_dotenv
# from services.text_extraction import extract_text
# from services.data_parsing import parse_invoice_data
# from services.database_service import store_invoice_data
# import os

# # Load environment variables
# load_dotenv()

# # Create uploads and outputs directories if they don't exist
# os.makedirs("uploads", exist_ok=True)
# os.makedirs("outputs", exist_ok=True)

# # Streamlit app
# st.title("Invoice OCR and Data Extraction")

# # Upload PDF
# uploaded_file = st.file_uploader("Upload a PDF invoice", type=["pdf", "jpg", "png"])
# print(f"Type of uploaded file: {type(uploaded_file)}")
# if uploaded_file is not None:
#     try:
#         # Extract text using Azure OCR
#         extracted_text = extract_text(uploaded_file)
#         st.write("Extracted Text:")
#         st.text(extracted_text)
#         print(f"Type of extracted_text: {type(extracted_text)}")

#         # Parse extracted text into structured data
#         parsed_data = parse_invoice_data(extracted_text)
#         st.write("Parsed Data:")
#         st.json(parsed_data)
#         print(f"Type of parsed_data: {type(parsed_data)}")

#         # Store the parsed data in the database
#         store_data = store_invoice_data(parsed_data)
#         st.success("Data stored in the database!")

#         # Convert parsed data to CSV
#         csv_path = os.path.join("outputs", "extracted_invoice.csv")
#         df = pd.DataFrame([parsed_data])
#         df.to_csv(csv_path, index=False)

#         # Provide download link
#         st.download_button(
#             label="Download CSV",
#             data=df.to_csv(index=False).encode("utf-8"),
#             file_name="extracted_invoice.csv",
#             mime="text/csv",
#         )

#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")