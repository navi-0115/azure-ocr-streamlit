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

    # Convert SQLAlchemy model objects to a flattened list of dictionaries
    flattened_data = []
    for invoice in invoices:
        # Extract invoice data
        invoice_data = {
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

        # Extract invoice items data
        for association in invoice.invoice_items_association: 
            invoice_item = association.invoice_item  
            item_data = {
                "item_name": invoice_item.item_name,
                "quantity": invoice_item.quantity,
                "unit_price": invoice_item.unit_price,
                "amount": invoice_item.amount,
            }
            flattened_row = {**invoice_data, **item_data}
            flattened_data.append(flattened_row)

    return flattened_data
