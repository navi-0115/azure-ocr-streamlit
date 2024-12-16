from datetime import datetime
from models.database_config import get_db_session
from models.invoice_model import Invoice

def store_invoice_data(data):
    session = get_db_session()
    try:
        # Convert Chinese date format to YYYY-MM-DD
        issue_date = datetime.strptime(data["issue_date"].replace("年", "-").replace("月", "-").replace("日", ""), "%Y-%m-%d").date()
        
        invoice = Invoice(
            invoice_number=data["invoice_number"],
            buyer_name=data["buyer_name"],
            buyer_address=data.get("buyer_address"),
            issue_date=issue_date,
            order_id=data["order_id"],
            items=data.get["items"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
            subtotal=data["subtotal"],
            amount=data["amount"],
            discount=data.get("discount"),
            shipping_cost=data.get("shipping_cost"),
            outstanding_balance=data.get("outstanding_amount"),
            total_amount=data["total_amount"],
            notes=data.get("notes"),
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()