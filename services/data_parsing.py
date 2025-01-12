import re
from datetime import datetime

def parse_invoice_data(text):
    """
    Parse extracted text into structured data.
    """
    # Debugging output
    print(f"DEBUG: Received text: '{text}'")

    # Regex patterns for the required fields
    patterns = {
        "invoice_number": r"FU\s*\d+", 
        "unified_number": r"統一編號[:：]\s*(\d+)",  
        "date": r"\d+\s*年\s*\d+\s*月\s*\d+\s*日",  
        "amount": r"應稅銷售額合計[:：]\s*([\d,]+)", 
        "tax": r"營業稅[:：]\s*([\d,]+)",  
        "total_amount": r"總計[:：]\s*([\d,]+)",  
    }

    # Initialize parsed data dictionary
    parsed_data = {}

    # Loop through patterns to find matches
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            if field == "date":
                raw_date = match.group(0).strip()
                parsed_data[field] = convert_date_format(raw_date)
            else:
                parsed_data[field] = match.group(0).strip() if field in ["invoice_number"] else match.group(1).strip()

    # Parse item (column up and down format)
    item_pattern = r"品名\s*[\n\r]+(.+?)\s*[\n\r]+"
    item_match = re.search(item_pattern, text, re.DOTALL)
    if item_match:
        # Extract only the item name (remove any additional text)
        item_name = item_match.group(1).strip()
        parsed_data["item"] = item_name.split("\n")[0].strip()  # Take the first line only

    return parsed_data


def convert_date_format(raw_date):
    """
    Convert date format from "113 年 12 月 3 日" to "yyyy-mm-dd".
    """
    # Extract year, month, and day using regex
    date_pattern = r"(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日"
    match = re.search(date_pattern, raw_date)
    if match:
        year = int(match.group(1)) + 1911 
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"
    return raw_date 