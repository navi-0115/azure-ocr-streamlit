import re

def normalize_invoice_type(invoice_type):
    """
    Normalize the invoice type to "統一發票(三聯式)" if it matches any of the incomplete or incorrect formats.
    """
    if not invoice_type:
        return invoice_type

    # Define patterns to match incomplete or incorrect invoice types
    patterns = [
        r"統[\s\-_]?發票[\s\-_]?\(?三聯式\)?",
        r"統[\s\-_]?發票[\s\-_]?三聯式\)?",
        r"統[\s\-_]?發票[\s\-_]?\(?三聯式",
    ]

    # Check if the invoice type matches any of the patterns
    for pattern in patterns:
        if re.match(pattern, invoice_type):
            return "統一發票(三聯式)"

    # If no match, return the original invoice type
    return invoice_type