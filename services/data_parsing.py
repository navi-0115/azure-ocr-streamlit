def parse_invoice_data(text):
    # Basic parsing logic (customize as needed)
    lines = text.split('\n')
    parsed_data = {}
    for line in lines:
        if "購買方名稱：" in line:
            parsed_data["buyer_name"] = line.split("：")[1].strip()
        elif "地址：" in line:
            parsed_data["buyer_address"] = line.split("：")[1].strip()
        elif "電話：" in line:
            parsed_data["buyer_phone"] = line.split("：")[1].strip()
        elif "纳税人识别号：" in line:
            parsed_data["buyer_tax_id"] = line.split("：")[1].strip()
        elif "销售方名称：" in line:
            parsed_data["seller_name"] = line.split("：")[1].strip()
        elif "发票号码：" in line:
            parsed_data["invoice_number"] = line.split("：")[1].strip()
        elif "开票日期：" in line:
            parsed_data["issue_date"] = line.split("：")[1].strip()
        elif "付款方式：" in line:
            parsed_data["payment_method"] = line.split("：")[1].strip()
        elif "小计：" in line:
            parsed_data["subtotal"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "税率：" in line:
            parsed_data["tax_rate"] = float(line.split("：")[1].replace("%", ""))
        elif "税额：" in line:
            parsed_data["tax_amount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "合计（小写）：" in line:
            parsed_data["total_amount"] = float(line.split("：")[1].replace("¥", "").replace(",", ""))
        elif "备注：" in line:
            parsed_data["remarks"] = line.split("：")[1].strip()
    return parsed_data
