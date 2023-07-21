"""Cria tabelas de contas a pagar e receber

Revision ID: c873272870f3
Revises: 
Create Date: 2023-07-16 10:24:50.055449

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c873272870f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('app',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('descricao', sa.String(length=30), nullable=True),
                    sa.Column('valor', sa.Numeric(), nullable=True),
                    sa.Column('tipo', sa.String(length=30), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('app')
