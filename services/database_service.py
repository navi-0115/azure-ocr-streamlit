from datetime import datetime
from models.database_config import get_db_session
from models.invoice_model import Invoice

def store_invoice_data(data):
    session = get_db_session()
    try:
        # Convert cleaned string to date
        # try:
        #     issue_date = datetime.strptime(cleaned_issue_date, "%Y-%m-%d").date()
        # except ValueError as e:
        #     raise ValueError(f"Failed to parse issue_date '{cleaned_issue_date}': {e}")
        
        # print(f"Parsed issue_date: {issue_date}")  # Debugging
        
        invoice = Invoice(
            invoice_number=data.get("invoice_number"),
            unified_number=data.get("unified_number"),
            issue_date=data.get("issue_date"),
            items=data.get("items"),
            tax=data.get("tax"),
            amount=data.get("amount"),
            total_amount=data.get("total_amount"),
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()