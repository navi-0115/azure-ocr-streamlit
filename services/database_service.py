from datetime import datetime
from models.database_init import get_db_session
from models.invoice_model import Invoice
from models.invoice_items_model import InvoiceItems
from models.invoice_types_model import InvoiceTypes

def store_invoice_data(data):
    session = get_db_session()
    try:
        
        invoice = Invoice(
            invoice_number=data.get("invoice_number"),
            invoice_type_id=data.get("invoice_type_id"),
            unified_number=data.get("unified_number"),
            issue_date=data.get("issue_date"),
            invoice_items_id=data.get("invoice_items_id"),
            total_before_tax=data.get("total_before_tax"),
            tax=data.get("tax"),
            total_after_tax=data.get("total_after_tax"),
        )
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
def store_invoice_items_data(data):
    session = get_db_session()
    try:
        
        invoice_items = InvoiceItems(
            invoice_id=data.get("invoice_id"),
            item_name=data.get("item_name"),
            quantity=data.get("quantity"),
            unit_price=data.get("unit_price"),
            amount=data.get("amount"),
        )
        session.add(invoice_items)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
        
def store_invoice_types_data(data):
    session = get_db_session()
    try:
        
        invoice_types = InvoiceTypes(
            name=data.get("name"),
        )
        session.add(invoice_types)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()