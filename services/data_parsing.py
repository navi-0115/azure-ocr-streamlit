import re
from datetime import datetime

def parse_invoice_data(text):
    if hasattr(text, "read"): 
        text = text.read().decode("utf-8")
    
    print(f"DEBUG: Received text: '{text}'")

    # Regex patterns for the required fields
    patterns = {
        "invoice_number": r"FU\s*\d+", 
        "unified_number": r"統一編號[:：]\s*(\d+)",  
        "issue_date": r"\d+\s*年\s*\d+\s*月\s*\d+\s*日",  
        "invoice_type": r"(統一發票（三聯式）|統發票（三聯式）|二聯式收銀機統一發票（長條型）|收銀機統一發票（三聯副聯式）|電子發票證明聯|載具號碼憑證|海關進口貨物稅費繳納)",  
        "items": r"品名\s*[\n\r]+(.+?)\s*[\n\r]+",
        "total_before_tax": r"應稅銷售額合計[:：]\s*([\d,]+)", 
        "tax": r"營業稅[:：]\s*([\d,]+)",  
        "total_after_tax": r"總計[:：]\s*([\d,]+)",  
    }

    # Initialize parsed data dictionary
    parsed_data = {}

    # Loop through patterns to find matches
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            if field == "issue_date":
                raw_date = match.group(0).strip()
                parsed_data[field] = convert_date_format(raw_date)
            elif field == "invoice_type":
                # Handle multiple possible invoice types
                invoice_type = match.group(1).strip()
                if "統一發票（三聯式）" in invoice_type or "統發票（三聯式）" in invoice_type:
                    parsed_data[field] = "統一發票（三聯式）"
                elif "二聯式收銀機統一發票（長條型）" in invoice_type:
                    parsed_data[field] = "二聯式收銀機統一發票（長條型）"
                elif "收銀機統一發票（三聯副聯式）" in invoice_type or "電子發票證明聯" in invoice_type or "載具號碼憑證" in invoice_type:
                    parsed_data[field] = "收銀機統一發票（三聯副聯式）"
                elif "海關進口貨物稅費繳納" in invoice_type:
                    parsed_data[field] = "海關進口貨物稅費繳納"
                else:
                    parsed_data[field] = "Unknown"
            else:
                parsed_data[field] = match.group(0).strip() if field in ["invoice_number"] else match.group(1).strip()

    # Parse items (column up and down format)
    item_pattern = r"品名\s*[\n\r]+(.+?)\s*[\n\r]+"
    item_match = re.search(item_pattern, text, re.DOTALL)
    if item_match:
        # Extract item details
        item_lines = item_match.group(1).strip().split("\n")
        parsed_data["invoice_items"] = []

        for line in item_lines:
            # Split the line into item name, quantity, unit price, and amount
            item_parts = line.strip().split()
            if len(item_parts) >= 4:
                item_name = " ".join(item_parts[:-3])  # Item name may contain spaces
                quantity = int(item_parts[-3].replace(",", ""))
                unit_price = float(item_parts[-2].replace(",", ""))
                amount = float(item_parts[-1].replace(",", ""))

                parsed_data["invoice_items"].append({
                    "item_name": item_name,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "amount": amount
                })

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