def parse_invoice_data(text):
    # Basic parsing logic (customize as needed)
    lines = text.split('\n')
    parsed_data = {
        "invoice_number": lines[0] if lines else None,
        "date": lines[1] if len(lines) > 1 else None,
        "items": lines[2:] if len(lines) > 2 else [],
    }
    return parsed_data
