import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import os

def extract_text(uploaded_file):
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

    # Read file content
    with uploaded_file.stream as image_stream:
        read_response = computervision_client.read_in_stream(image_stream, raw=True)

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
