def parse_invoice_data(text):
    # Basic parsing logic (customize as needed)
    lines = text.split('\n')
    parsed_data = {}
    for line in lines:
        if "發票號碼：" in line:
            parsed_data["invoice_number"] = line.split("：")[1].strip()
        elif "付款對象：" in line:
            parsed_data["buyer_name"] = line.split("：")[1].strip()
        elif "運送至：" in line:
            parsed_data["buyer_address"] = line.split("：")[1].strip()
        elif "日期：" in line:
            parsed_data["issue_date"] = line.split("：")[1].strip()
        elif "訂單 ID：" in line:
            parsed_data["order_id"] = line.split("：")[1].strip()
        elif "項目：" in line:
            parsed_data["item"] = line.split("：")[1].strip()
        elif "數量：" in line:
            parsed_data["quantity"] = line.split("：")[1].strip()
        elif "價格：" in line:
            parsed_data["unit_price"] = line.split("：")[1].strip()
        elif "金額：" in line:
            parsed_data["amount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "小計：" in line:
            parsed_data["subtotal"] = float(line.split("：")[1].replace("%", ""))
        elif "折扣：" in line:
            parsed_data["discount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "運費：" in line:
            parsed_data["shipping_cost"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "备注：" in line:
            parsed_data["total_amount"] = line.split("：")[1].strip()
        elif "總計：" in line:
            parsed_data["outstanding_balance"] = line.split("：")[1].strip()
        elif "備註：" in line:
            parsed_data["notes"] = line.split("：")[1].strip()
    return parsed_data
