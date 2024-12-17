import re
def parse_invoice_data(text):
        # Debugging output
    print(f"DEBUG: Received text: '{text}'")
    
    # Define regex patterns for different fields
    patterns = {
        "invoice_number": r"發票號碼[:：]\s*(\d+)",  # Matches '發票號碼: 39519'
        "issue_date": r"日期[:：]\s*([\d年月日]+)",   # Matches '日期: 2012年2月19日'
        "buyer_name": r"付款對象[:：]\s*(.+)",       # Matches '付款對象: Aaron Bergman'
        "buyer_address": r"運送至[:：]\s*(.+)",      # Matches '運送至: 76017, Arlington, Texas, United States'
        "outstanding_balance": r"到期餘額[:：]\s*\$(\d+\.\d+)",  # Matches '到期餘額: $22.17'
        "subtotal": r"小計[:：]\s*\$(\d+\.\d+)",     # Matches '小計: $25.25'
        "discount": r"折扣.*:\s*\$(\d+\.\d+)",      # Matches '折扣(20%): $5.05'
        "shipping_cost": r"運費[:：]\s*\$(\d+\.\d+)",  # Matches '運費: $1.97'
        "total_amount": r"總計[:：]\s*\$(\d+\.\d+)",  # Matches '總計: $22.17'
        "order_id": r"訂單ID[:：]\s*(\S+)",         # Matches '訂單ID: CA-2012-AB10015140-40958'
        "notes": r"備註[:：]\s*(.+)",               # Matches '備註: 感謝您的業務!'
    }
    
    # Initialize parsed data dictionary
    parsed_data = {}
    
        # Loop through patterns to find matches
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            parsed_data[field] = match.group(1)  # Extract captured group
    
    # Additional Parsing for Items Section
    items_pattern = r"(.+?)\s+(\d+)\s+\$(\d+\.\d+)"  # Matches: item_name, quantity, price
    items = []
    items_section_start = False
    
    for line in text.splitlines():
        line = line.strip()
        if "項目" in line:  # Start of items section
            items_section_start = True
            continue
        if items_section_start and line.startswith("小計"):  # End of items section
            break
        
        # Match item lines with regex
        item_match = re.match(items_pattern, line)
        if item_match:
            item_name = item_match.group(1).strip()
            quantity = int(item_match.group(2))
            price = float(item_match.group(3))
            items.append({
                "item_name": item_name,
                "quantity": quantity,
                "price": price
            })
    
    if items:
        parsed_data["items"] = items
    
    # Adjust issue_date format to 'YYYY-MM-DD'
    if "issue_date" in parsed_data:
        parsed_data["issue_date"] = parsed_data["issue_date"].replace("年", "-").replace("月", "-").replace("日", "")
    
    return parsed_data
    
    # # Basic parsing logic (customize as needed)
    # print(f"DEBUG: Received text: '{text}'")  # Check if text contains anything
    # lines = text.split("\n")  # Split into lines
    # print(f"DEBUG: Split lines: {lines}")    # Check split lines
    
    # parsed_data = {}
    # for line in lines:
    #     line = line.strip() 
    #     if "發票號碼：" in line:
    #         parsed_data["invoice_number"] = line.split("：")[1].strip()
    #     elif "付款對象：" in line:
    #         parsed_data["buyer_name"] = line.split("：")[1].strip()
    #     elif "運送至：" in line:
    #         parsed_data["buyer_address"] = line.split("：")[1].strip()
    #     elif "日期：" in line:
    #         raw_date = line.split(":")[1].strip()
    #         parsed_data["issue_date"] = raw_date.replace("年", "-").replace("月", "-").replace("日", "").strip()
    #     elif "訂單 ID：" in line:
    #         parsed_data["order_id"] = line.split("：")[1].strip()
    #     elif "項目：" in line:
    #         parsed_data["items"] = line.split("：")[1].strip()
    #     elif "數量：" in line:
    #         parsed_data["quantity"] = line.split("：")[1].strip()
    #     elif "價格：" in line:
    #         parsed_data["unit_price"] = line.split("：")[1].strip()
    #     elif "金額：" in line:
    #         parsed_data["amount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
    #     elif "小計：" in line:
    #         parsed_data["subtotal"] = float(line.split("：")[1].replace("%", ""))
    #     elif "折扣：" in line:
    #         parsed_data["discount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
    #     elif "運費：" in line:
    #         parsed_data["shipping_cost"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
    #     elif "备注：" in line:
    #         parsed_data["total_amount"] = line.split("：")[1].strip()
    #     elif "總計：" in line:
    #         parsed_data["outstanding_balance"] = line.split("：")[1].strip()
    #     elif "備註：" in line:
    #         parsed_data["notes"] = line.split("：")[1].strip()
    #     print(f"parsed_data: {parsed_data}")
    # return parsed_data
