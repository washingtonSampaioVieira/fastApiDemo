"""Adiciona colunas de controle de baixa para contas

Revision ID: 2d831cbf1815
Revises: bc6131ef36e2
Create Date: 2023-07-18 19:24:49.413385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d831cbf1815'
down_revision = 'bc6131ef36e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app', sa.Column('data_baixa', sa.DateTime(), nullable=True))
    op.add_column('app', sa.Column('valor_da_baixa', sa.Numeric(), nullable=True))
    op.add_column('app', sa.Column('esta_baixada', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('app', 'esta_baixada')
    op.drop_column('app', 'valor_da_baixa')
    op.drop_column('app', 'data_baixa')
    # ### end Alembic commands ###
