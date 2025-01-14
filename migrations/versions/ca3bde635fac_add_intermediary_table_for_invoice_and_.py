"""add intermediary table for invoice  and invoice items in model

Revision ID: ca3bde635fac
Revises: 16f95a934f64
Create Date: 2025-01-13 22:41:21.156696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca3bde635fac'
down_revision: Union[str, None] = '16f95a934f64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice_items_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_id', sa.Integer(), nullable=False),
    sa.Column('invoice_item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
    sa.ForeignKeyConstraint(['invoice_item_id'], ['invoice_items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoice_items_association_id'), 'invoice_items_association', ['id'], unique=False)
    op.add_column('invoice_items', sa.Column('created_at', sa.TIMESTAMP(), nullable=False))
    op.add_column('invoice_items', sa.Column('updated_at', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_items', 'updated_at')
    op.drop_column('invoice_items', 'created_at')
    op.drop_index(op.f('ix_invoice_items_association_id'), table_name='invoice_items_association')
    op.drop_table('invoice_items_association')
    # ### end Alembic commands ###
