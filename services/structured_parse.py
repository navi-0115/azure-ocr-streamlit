import re
from datetime import datetime

def parse_invoice_data(structured_data):
    """
    Parse structured data extracted from the Azure Document Intelligence API.
    """
    print("structured data in parsing logic:", structured_data)
    parsed_data = {}

    
    # Extract and process fields
    parsed_data["invoice_number"] = structured_data.get("invoice_number", "")
    parsed_data["unified_number"] = structured_data.get("unified_number", "")
    parsed_data["issue_date"] = convert_date_format(structured_data.get("issue_date", ""))
    parsed_data["invoice_type"] = structured_data.get("invoice_type", "")
    parsed_data["total_before_tax"] = float(structured_data.get("total_before_tax", "0").replace(",", ""))
    parsed_data["tax"] = float(structured_data.get("tax", "0").replace(",", ""))
    parsed_data["total_after_tax"] = float(structured_data.get("total_after_tax", "0").replace(",", ""))

    # Process invoice items
    parsed_data["invoice_items"] = []
    for item in structured_data.get("invoice_items", []):
        parsed_data["invoice_items"].append({
            "item_name": item.get("item_name", ""),
            "quantity": int(item.get("quantity", "0")),
            "unit_price": float(item.get("unit_price", "0").replace(",", "")),
            "amount": float(item.get("amount", "0").replace(",", "")),
        })

    print("parsed data in file logic:", parsed_data)
    return parsed_data

def convert_date_format(raw_date):
    """
    Convert date format from "113年12月9日" to "yyyy-mm-dd".
    """
    date_pattern = r"(\d+)年(\d+)月(\d+)日"
    match = re.search(date_pattern, raw_date)
    if match:
        year = int(match.group(1)) + 1911
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    return raw_date