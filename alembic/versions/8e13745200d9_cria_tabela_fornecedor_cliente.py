"""Cria tabela fornecedor cliente

Revision ID: 8e13745200d9
Revises: c873272870f3
Create Date: 2023-07-16 18:57:28.681904

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8e13745200d9'
down_revision = 'c873272870f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('fornecedor_cliente',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('nome', sa.String(length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('fornecedor_cliente')
