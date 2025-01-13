from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
import json
from dotenv import load_dotenv

load_dotenv()

def extract_text(uploaded_file):
    key = os.getenv("AZURE_SERVICE_KEY")
    endpoint = os.getenv("AZURE_SERVICE_ENDPOINT")
    model_id = os.getenv("AZURE_MODEL_ID")
    
    if not key or not endpoint:
        raise ValueError("Azure credentials (key or endpoint) are missing. Check your environment variables.")

    # Initialize the client
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    file_base64_content = uploaded_file.read()

    try:
        # Analyze the document
        poller = document_intelligence_client.begin_analyze_document(
            model_id=model_id, 
            body=file_base64_content,
            locale="zh-hant-tw"
        )
        
        # Wait for the operation to complete
        print("Processing the document with Azure Document Intelligence...")
        result = poller.result()
        print("Analysis completed.")

        # Extract structured data from the result
        structured_data = extract_structured_data(result)
        return structured_data
            
    except Exception as e:
        print(f"An error occurred during document analysis: {e}")
        raise e

def extract_structured_data(result):
    """
    Extract structured data from the Azure Document Intelligence API response.
    """
    structured_data = {}

    if result.documents:
        for document in result.documents:
            # Extract fields from the document
            fields = document.fields
            structured_data["invoice_number"] = fields.get("invoice_number", {}).get("content", "").strip()
            structured_data["unified_number"] = fields.get("unified_number", {}).get("content", "").strip()
            structured_data["issue_date"] = fields.get("issue_date", {}).get("content", "").strip()
            structured_data["invoice_type"] = fields.get("invoice_type", {}).get("content", "").strip()
            structured_data["total_before_tax"] = fields.get("total_before_tax", {}).get("content", "").strip()
            structured_data["tax"] = fields.get("tax", {}).get("content", "").strip()
            structured_data["total_after_tax"] = fields.get("total_after_tax", {}).get("content", "").strip()

            # Extract invoice items
            invoice_items = []
            items_field = fields.get("invoice_items", {})
            if items_field.get("type") == "array":
                for item in items_field.get("valueArray", []):
                    item_data = {
                        "item_name": item.get("valueObject", {}).get("item_name", {}).get("content", "").strip(),
                        "quantity": item.get("valueObject", {}).get("quantity", {}).get("content", "").strip(),
                        "unit_price": item.get("valueObject", {}).get("unit_price", {}).get("content", "").strip(),
                        "amount": item.get("valueObject", {}).get("amount", {}).get("content", "").strip(),
                    }
                    invoice_items.append(item_data)
            structured_data["invoice_items"] = invoice_items

    return structured_data