"""empty message

Revision ID: 67d1dd824098
Revises: 69efe2fd6894
Create Date: 2019-12-19 18:53:43.646914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67d1dd824098'
down_revision = '69efe2fd6894'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('car_data')
    op.add_column('car_data_value', sa.Column('code_type', sa.Integer(), nullable=False))
    op.drop_constraint(None, 'car_data_value', type_='foreignkey')
    op.drop_column('car_data_value', 'id_CarData')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car_data_value', sa.Column('id_CarData', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'car_data_value', 'car_data', ['id_CarData'], ['id'])
    op.drop_column('car_data_value', 'code_type')
    op.create_table('car_data',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('carDataName', sa.VARCHAR(length=100), nullable=False),
    sa.Column('dataType', sa.BOOLEAN(), nullable=False),
    sa.CheckConstraint('"dataType" IN (0, 1)'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###