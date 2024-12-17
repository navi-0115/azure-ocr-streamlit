from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.text_extraction import extract_text
from services.data_parsing import parse_invoice_data
from services.database_service import store_invoice_data
import os

load_dotenv()

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def process_invoice():
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return jsonify({"error": "Empty file uploaded"}), 400

        # Extract text using Azure OCR
        extracted_text = extract_text(uploaded_file)
        print(f"Full extract data: {extracted_text}")


        # Parse extracted text into structured data
        parsed_data = parse_invoice_data(extracted_text)
        print(f"Full parsed data: {parsed_data}")
        print(type(parsed_data))  # Should print <class 'dict'>
        print(parsed_data.keys()) 

        # Store the parsed data in the database
        store_invoice_data(parsed_data)
        

        return jsonify({"message": "Invoice processed successfully", "data": parsed_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
