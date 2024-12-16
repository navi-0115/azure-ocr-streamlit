from flask import Flask, request, jsonify
import os
import time
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

load_dotenv()
app = Flask(__name__)

# Create the local storage directory if it doesn't exist
LOCAL_STORAGE_DIR = "extracted_text"
os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)

# Temporary directory for uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_text(file_path, computervision_client):
    with open(file_path, "rb") as image_stream:
        # Analyze file using Azure OCR
        read_response = computervision_client.read_in_stream(image_stream, raw=True)

    # Get the operation location (URL with an ID at the end)
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Retrieve the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ["notstarted", "running"]:
            break
        time.sleep(1)

    # Extract the detected text
    text = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for page in read_result.analyze_result.read_results:
            for line in page.lines:
                # Add text line by line
                text += line.text + "\n"

    return text.strip()

@app.route('/ocr', methods=['POST'])
def process_invoice():
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return jsonify({"error": "Empty file uploaded"}), 400

        # Save the uploaded file
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        uploaded_file.save(file_path)

        # Load Azure credentials
        key = os.getenv("COG_SERVICE_KEY")
        region = os.getenv("COG_SERVICE_REGION")
        COG_endpoint = os.getenv("COG_SERVICE_ENDPOINT")

        # Initialize Azure OCR client
        computervision_client = ComputerVisionClient(COG_endpoint, CognitiveServicesCredentials(key))

        # Extract text using Azure OCR
        extracted_text = get_text(file_path, computervision_client)

        # Save the extracted text to a file in the local storage directory
        timestamp = int(time.time())  # Use a timestamp to create unique filenames
        output_filename = uploaded_file.filename.split('.')[0] + '_' + str(timestamp) + '.txt'
        output_path = os.path.join(LOCAL_STORAGE_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(extracted_text)

        # Cleanup the uploaded file
        os.remove(file_path)

        return jsonify({"message": "Text extracted and saved successfully", "file": output_filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


