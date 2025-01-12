import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import os
from io import BytesIO  

from dotenv import load_dotenv

load_dotenv()

def extract_text(uploaded_file):
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

    # Read file content
    file_content = uploaded_file.read()  # Get the file content as bytes

    # Wrap the bytes in a file-like object (BytesIO)
    file_like_object = BytesIO(file_content)

    # Use the file-like object with the Azure Computer Vision API
    read_response = computervision_client.read_in_stream(file_like_object, raw=True)

    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Wait for OCR operation to complete
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ["notstarted", "running"]:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        text = "\n".join(
            line.text for page in read_result.analyze_result.read_results for line in page.lines
        )
        return text.strip()
    else:
        raise Exception("Text extraction failed")