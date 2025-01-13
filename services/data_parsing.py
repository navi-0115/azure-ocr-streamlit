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
        "total_before_tax": r"應稅銷售額合計[:：]\s*([\d,]+)",
        "tax": r"營業稅[:：]\s*([\d,]+)",
        "total_after_tax": r"總計[:：]\s*([\d,]+)",
    }

    # Initialize parsed data dictionary
    parsed_data = {"items": []}

    # Loop through patterns to find matches
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            if field == "issue_date":
                raw_date = match.group(0).strip()
                parsed_data[field] = convert_date_format(raw_date)
            else:
                parsed_data[field] = match.group(1).replace(",", "").strip()

    # Parse items (multi-line format for each item)
    item_pattern = r"品名\s+(\S+)\s+(\d+)\s+([\d,]+)\s+([\d,]+)"
    for item_match in re.finditer(item_pattern, text):
        item_data = {
            "item_name": item_match.group(1).strip(),
            "quantity": int(item_match.group(2)),
            "unit_price": float(item_match.group(3).replace(",", "")),
            "amount": float(item_match.group(4).replace(",", "")),
        }
        parsed_data["items"].append(item_data)

    return parsed_data


def convert_date_format(raw_date):
    """
    Convert date format from "113 年 12 月 3 日" to "YYYY-MM-DD".
    """
    # Extract year, month, and day using regex
    date_pattern = r"(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日"
    match = re.search(date_pattern, raw_date)
    if match:
        year = int(match.group(1)) + 1911  # Adjust year from ROC to Gregorian
        month = int(match.group(2))
        day = int(match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    return raw_date



# import re
# from datetime import datetime

# def parse_invoice_data(text):

#     if hasattr(text, "read"): 
#         text = text.read().decode("utf-8")
    
#     print(f"DEBUG: Received text: '{text}'")

#     # Regex patterns for the required fields
#     patterns = {
#         "invoice_number": r"FU\s*\d+", 
#         "unified_number": r"統一編號[:：]\s*(\d+)",  
#         "issue_date": r"\d+\s*年\s*\d+\s*月\s*\d+\s*日",  
#         "items": r"品名\s*[\n\r]+(.+?)\s*[\n\r]+",
#         "amount": r"應稅銷售額合計[:：]\s*([\d,]+)", 
#         "tax": r"營業稅[:：]\s*([\d,]+)",  
#         "total_amount": r"總計[:：]\s*([\d,]+)",  
#     }

#     # Initialize parsed data dictionary
#     parsed_data = {}

#     # Loop through patterns to find matches
#     for field, pattern in patterns.items():
#         match = re.search(pattern, text)
#         if match:
#             if field == "issue_date":
#                 raw_date = match.group(0).strip()
#                 parsed_data[field] = convert_date_format(raw_date)
#             else:
#                 parsed_data[field] = match.group(0).strip() if field in ["invoice_number"] else match.group(1).strip()

#     # Parse item (column up and down format)
#     item_pattern = r"品名\s*[\n\r]+(.+?)\s*[\n\r]+"
#     item_match = re.search(item_pattern, text, re.DOTALL)
#     if item_match:
#         # Extract only the item name (remove any additional text)
#         item_name = item_match.group(1).strip()
#         parsed_data["items"] = item_name.split("\n")[0].strip()  # Take the first line only

#     return parsed_data


# def convert_date_format(raw_date):
#     """
#     Convert date format from "113 年 12 月 3 日" to "yyyy-mm-dd".
#     """
#     # Extract year, month, and day using regex
#     date_pattern = r"(\d+)\s*年\s*(\d+)\s*月\s*(\d+)\s*日"
#     match = re.search(date_pattern, raw_date)
#     if match:
#         year = int(match.group(1)) + 1911 
#         month = int(match.group(2))
#         day = int(match.group(3))
#         return f"{year:04d}-{month:02d}-{day:02d}"

#     return raw_date 