from utils.invoice_number_rules import INVOICE_NUMBER_RULES

def validate_invoice_number(invoice_number, issue_date, invoice_type_code):
    """
    Validate the invoice number based on the issue date and invoice type code.
    """
    if not invoice_number or not issue_date or not invoice_type_code:
        return False, "Missing required fields for validation."

    # Extract the month from the issue date
    try:
        issue_month = int(issue_date.split("-")[1])  # Extract month from "yyyy-mm-dd"
    except (IndexError, ValueError):
        return False, "Invalid issue date format."

    # Get the rules for the invoice type code
    rules = INVOICE_NUMBER_RULES.get(invoice_type_code)
    if not rules:
        return False, f"No validation rules found for invoice type code {invoice_type_code}."

    # Find the expected prefix for the issue month
    expected_prefix = None
    for month_range, prefix in rules.items():
        if month_range[0] <= issue_month <= month_range[1]:
            expected_prefix = prefix
            break

    if not expected_prefix:
        return False, f"No prefix rule found for month {issue_month}."

    # Check if the invoice number starts with the expected prefix
    if not invoice_number.startswith(expected_prefix):
        return False, f"Invoice number '{invoice_number}' does not match the expected prefix '{expected_prefix}' for month {issue_month}."

    return True, "Validation successful."