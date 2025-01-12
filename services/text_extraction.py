# import time
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# import os
# from io import BytesIO  

# from dotenv import load_dotenv

# load_dotenv()

# def extract_text(uploaded_file):
#     key = os.getenv("AZURE_SERVICE_KEY")
#     endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")

#     computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

#     # Read file content
#     file_content = uploaded_file.read()  # Get the file content as bytes

#     # Wrap the bytes in a file-like object (BytesIO)
#     file_like_object = BytesIO(file_content)

#     # Use the file-like object with the Azure Computer Vision API
#     read_response = computervision_client.read_in_stream(file_like_object, raw=True)

#     read_operation_location = read_response.headers["Operation-Location"]
#     operation_id = read_operation_location.split("/")[-1]

#     # Wait for OCR operation to complete
#     while True:
#         read_result = computervision_client.get_read_result(operation_id)
#         if read_result.status.lower() not in ["notstarted", "running"]:
#             break
#         time.sleep(1)

#     if read_result.status == OperationStatusCodes.succeeded:
#         text = "\n".join(
#             line.text for page in read_result.analyze_result.read_results for line in page.lines
#         )
#         return text.strip()
#     else:
#         raise Exception("Text extraction failed")
    
    
#     import time
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
import os
from io import BytesIO 

from dotenv import load_dotenv
load_dotenv()

def extract_text(uploaded_file):
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")

    # Initialize the client
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    document_content = uploaded_file.read()

    # Read file content
    poller = document_intelligence_client.begin_analyze_document(
            model_id="prebuilt-layout", body=document_content
        )
    
    print(poller)
    
    # Wait for the operation to complete
    result  = poller.result()
    print(type(result))

    # Extract text from the result
    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content
    return extracted_text.strip()   
