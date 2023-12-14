"""Inventory and Schedules table

Revision ID: 3e4ea1d3c842
Revises: a70f3a1c8346
Create Date: 2023-12-14 14:38:37.596642

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3e4ea1d3c842'
down_revision = 'a70f3a1c8346'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('brand_name', sa.Text(), nullable=True),
    sa.Column('medicine_name', sa.Text(), nullable=True),
    sa.Column('dosage', sa.Numeric(), nullable=True),
    sa.Column('dosage_unit', sa.Integer(), nullable=True),
    sa.Column('stock', sa.Text(), nullable=True),
    sa.Column('medication_type', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('inventory_id')
    )
    op.create_table('schedule',
    sa.Column('schedule_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('schedule_state', sa.Integer(), nullable=True),
    sa.Column('time_to_take', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('quantity', sa.Numeric(), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('schedule_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule')
    op.drop_table('inventory')
    # ### end Alembic commands ###
