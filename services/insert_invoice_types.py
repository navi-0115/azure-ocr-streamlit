from sqlalchemy.orm import Session
from models.database_config import get_db_session
from models.invoice_model import InvoiceTypes

def initialize_invoice_types():
    session = get_db_session()
    try:
        # Define hardcoded invoice types
        hardcoded_invoice_types = [
            {'code': '21', 'name': '統一發票(三聯式)'},
            {'code': '22', 'name': '二聯式收銀機統一發票(長條型)'},
            {'code': '25', 'name': '收銀機統一發票(三聯副聯式)'},
            {'code': '28', 'name': '海關進口貨物稅費繳納'},
        ]

        # Check if each invoice type exists, and insert if it doesn't
        for invoice_type_data in hardcoded_invoice_types:
            invoice_type = session.query(InvoiceTypes).filter_by(code=invoice_type_data['code']).first()
            if not invoice_type:
                invoice_type = InvoiceTypes(**invoice_type_data)
                session.add(invoice_type)
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Call this function during application startup
initialize_invoice_types()