from datetime import datetime
from models.database_config import get_db_session
from models.invoice_model import Invoice

def store_invoice_data(data):
    session = get_db_session()
    try:
        # Convert Chinese date format to YYYY-MM-DD
        issue_date = datetime.strptime(data["issue_date"].replace("年", "-").replace("月", "-").replace("日", ""), "%Y-%m-%d").date()
        
        invoice = Invoice(
            buyer_name=data["buyer_name"],
            buyer_address=data.get("buyer_address"),
            buyer_phone=data.get("buyer_phone"),
            buyer_tax_id=data.get("buyer_tax_id"),
            seller_name=data["seller_name"],
            seller_address=data.get("seller_address"),
            seller_phone=data.get("seller_phone"),
            seller_tax_id=data.get("seller_tax_id"),
            invoice_number=data["invoice_number"],
            issue_date=issue_date,
            payment_method=data.get("payment_method"),
            subtotal=data["subtotal"],
            tax_rate=data["tax_rate"],
            tax_amount=data["tax_amount"],
            total_amount=data["total_amount"],
            total_amount_in_words=data.get("total_amount_in_words"),
            remarks=data.get("remarks"),
            payee=data.get("payee"),
            bank_name=data.get("bank_name"),
            bank_account=data.get("bank_account"),
            items=data.get("items"),  # Ensure items is a JSON object
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()