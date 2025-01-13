from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest
import os
import base64
from io import BytesIO 
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

def load_file_as_base64(uploaded_file):

    file_data=uploaded_file.read()
    # base64_byte = base64.b64encode(file_data)
    # base64_string = base64_byte.decode("utf-8")
    print("file data:", file_data)
        
    return file_data

def extract_text(uploaded_file):
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")
    
    if not key or not endpoint:
        raise ValueError("Azure credentials (key or endpoint) are missing. Check your environment variables.")

    # Initialize the client
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    file_base64_content = uploaded_file.read()

    try:
        # Read file content
        poller = document_intelligence_client.begin_analyze_document(
                model_id="prebuilt-layout", 
                body=file_base64_content,
                locale = "zh-hant-tw"
            )
        
        # Wait for the operation to complete
        result  = poller.result()
        print("result type:", type(result))
        
        # Extract text from the result
        extracted_text = ""
        for page in result.pages:
            for line in page.lines:
                extracted_text += line.content + "\n"
        return extracted_text.strip()   
            
    except Exception as e:
        print(f"An error occurred during document analysis: {e}")

