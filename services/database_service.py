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
            buyer_name=data.get("buyer_name"),
            buyer_address=data.get("buyer_address"),
            issue_date=data.get("issue_date"),
            order_id=data.get("order_id"),
            items=data.get("items"),
            quantity=data.get("quantity"),
            unit_price=data.get("unit_price"),
            subtotal=data.get("subtotal"),
            amount=data.get("amount"),
            discount=data.get("discount"),
            shipping_cost=data.get("shipping_cost"),
            outstanding_balance=data.get("outstanding_balance"),
            total_amount=data.get("total_amount"),
            notes=data.get("notes"),
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()