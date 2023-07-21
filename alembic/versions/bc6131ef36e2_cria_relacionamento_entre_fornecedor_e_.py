"""Cria relacionamento entre fornecedor e conta

Revision ID: bc6131ef36e2
Revises: 8e13745200d9
Create Date: 2023-07-17 19:40:35.358320

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bc6131ef36e2'
down_revision = '8e13745200d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('app', sa.Column('fornecedor_client_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'app', 'fornecedor_cliente', ['fornecedor_client_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'app', type_='foreignkey')
    op.drop_column('app', 'fornecedor_client_id')
