from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.database_config import get_db_session
from models.invoice_model import Invoice, InvoiceItem, InvoiceTypes, InvoiceItemsAssociation
from utils.invoice_types import INVOICE_TYPES

def store_invoice_data(data):
    session = get_db_session()
    try:
        # Parse and store invoice type
        invoice_type_name = data.get("invoice_type")
        # Validate invoice type
        if invoice_type_name not in INVOICE_TYPES:
            raise ValueError(f"Invalid invoice type: {invoice_type_name}")

        invoice_type = session.query(InvoiceTypes).filter_by(name=invoice_type_name).first()
        if not invoice_type:
            invoice_type = InvoiceTypes(name=invoice_type_name)
            session.add(invoice_type)
            session.commit()

        # Parse and store invoice
        invoice = Invoice(
            invoice_number=data.get("invoice_number"),
            invoice_type_id=invoice_type.id,
            unified_number=data.get("unified_number"),
            issue_date=datetime.strptime(data.get("issue_date"), "%Y-%m-%d").date(),
            total_before_tax=float(data.get("total_before_tax", 0).replace(",", "")),
            tax=float(data.get("tax", 0).replace(",", "")),
            total_after_tax=float(data.get("total_after_tax", 0).replace(",", "")),
        )
        session.add(invoice)
        session.commit()

        # Parse and store invoice items
        for item in data.get("invoice_items", []):
            # Create InvoiceItem
            invoice_item = InvoiceItem(
                item_name=item.get("item_name"),
                quantity=item.get("quantity"),
                unit_price=item.get("unit_price"),
                amount=item.get("amount"),
            )
            session.add(invoice_item)
            session.commit()

            # Create association between Invoice and InvoiceItem
            association = InvoiceItemsAssociation(
                invoice_id=invoice.id,
                invoice_item_id=invoice_item.id
            )
            session.add(association)
            session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_recent_invoices(db: Session):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    return db.query(Invoice).filter(Invoice.created_at >= thirty_days_ago).all()

# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from models.database_config import get_db_session
# from models.invoice_model import Invoice, InvoiceItems, InvoiceTypes
# from utils.invoice_types import INVOICE_TYPES


# def store_invoice_data(data):
#     session = get_db_session()
#     try:
#         # Parse and store invoice type
#         invoice_type_name = data.get("invoice_type")
#         # Validate invoice type
#         if invoice_type_name not in INVOICE_TYPES:
#             raise ValueError(f"Invalid invoice type: {invoice_type_name}")

#         invoice_type = session.query(InvoiceTypes).filter_by(name=invoice_type_name).first()
#         if not invoice_type:
#             invoice_type = InvoiceTypes(name=invoice_type_name)
#             session.add(invoice_type)
#             session.commit()

#         # Parse and store invoice
#         invoice = Invoice(
#             invoice_number=data.get("invoice_number"),
#             invoice_type_id=invoice_type.id,
#             unified_number=data.get("unified_number"),
#             issue_date=datetime.strptime(data.get("issue_date"), "%Y-%m-%d").date(),
#             total_before_tax=float(data.get("total_before_tax", 0).replace(",", "")),
#             tax=float(data.get("tax", 0).replace(",", "")),
#             total_after_tax=float(data.get("total_after_tax", 0).replace(",", "")),
#         )
#         session.add(invoice)
#         session.commit()

#         # Parse and store invoice items
#         for item in data.get("invoice_items", []):
#             invoice_item = InvoiceItems(
#                 invoice_id=invoice.id,
#                 item_name=item.get("item_name"),
#                 quantity=item.get("quantity"),
#                 unit_price=item.get("unit_price"),
#                 amount=item.get("amount"),
#             )
#             session.add(invoice_item)
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()
        
# def get_recent_invoices(db: Session):
#     thirty_days_ago = datetime.now() - timedelta(days=30)
#     return db.query(Invoice).filter(Invoice.created_at >= thirty_days_ago).all()

# from datetime import datetime
# from models.database_config import get_db_session
# from models.invoice_model import Invoice

# def store_invoice_data(data):
#     session = get_db_session()
#     try:
        
#         invoice = Invoice(
#             invoice_number=data.get("invoice_number"),
#             unified_number=data.get("unified_number"),
#             issue_date=data.get("issue_date"),
#             items=data.get("items"),
#             tax=data.get("tax"),
#             amount=data.get("amount"),
#             total_amount=data.get("total_amount"),
#         )
#         session.add(invoice)
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()