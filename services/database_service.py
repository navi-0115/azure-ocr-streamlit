from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.database_config import get_db_session
from models.invoice_model import Invoice, InvoiceItem, InvoiceTypes, InvoiceItemsAssociation
from utils.invoice_types import INVOICE_TYPES

def store_invoice_data(data):
    session = get_db_session()
    try:
        invoice_type_name = data.get("invoice_type") 
        if not invoice_type_name:
            raise ValueError("Invoice type is missing in the data.")

        # Validate invoice type against INVOICE_TYPES values
        # valid_invoice_types = list(INVOICE_TYPES.values())
        # if invoice_type_name not in valid_invoice_types:
        #     raise ValueError(f"Invalid invoice type: {invoice_type_name}. Valid types are: {valid_invoice_types}")

        invoice_type = session.query(InvoiceTypes).filter_by(name=invoice_type_name).first()
        if not invoice_type:
            invoice_type = InvoiceTypes(name=invoice_type_name)
            session.add(invoice_type)
            session.commit()
            
        # Helper function to safely convert to float
        def to_float(value):
            if isinstance(value, str):
                return float(value.replace(",", ""))  
            elif isinstance(value, (int, float)):
                return float(value)  
            else:
                return 0.0 

        # Parse and store invoice
        invoice = Invoice(
            invoice_number=data.get("invoice_number"),
            invoice_type_id=invoice_type.id,
            unified_number=data.get("unified_number"),
            issue_date=datetime.strptime(data.get("issue_date"), "%Y-%m-%d").date(),
            total_before_tax=to_float(data.get("total_before_tax", 0)),
            tax=to_float(data.get("tax", 0)),
            total_after_tax=to_float(data.get("total_after_tax", 0)),
        )
        session.add(invoice)
        session.commit()

        # Parse and store invoice items
        for item in data.get("invoice_items", []):
            # Create InvoiceItem
            invoice_item = InvoiceItem(
                item_name=item.get("item_name"),
                quantity=int(item.get("quantity", 0)),  
                unit_price=to_float(item.get("unit_price", 0)),  
                amount=to_float(item.get("amount", 0)),  
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

def get_recent_invoices(db: Session, days: int = 30):
    start_date = datetime.now() - timedelta(days=days)
    invoices = db.query(Invoice).filter(Invoice.created_at >= start_date).all()

    # Convert SQLAlchemy model objects to dictionaries
    invoice_dicts = []
    for invoice in invoices:
        invoice_dict = {
            "invoice_number": invoice.invoice_number,
            "invoice_type": invoice.invoice_types.name if invoice.invoice_types else None,
            "unified_number": invoice.unified_number,
            "issue_date": invoice.issue_date.isoformat() if invoice.issue_date else None,
            "total_before_tax": invoice.total_before_tax,
            "tax": invoice.tax,
            "total_after_tax": invoice.total_after_tax,
            "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
            "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
        }
        invoice_dicts.append(invoice_dict)

    return invoice_dicts

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