"""Added birthdate and gender to users table.

Revision ID: 669a669eb646
Revises: b949ec822291
Create Date: 2023-12-04 12:20:10.999671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '669a669eb646'
down_revision = 'b949ec822291'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('forgot_password_identifier_key', 'forgot_password', type_='unique')
    op.add_column('users', sa.Column('birthdate', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'gender')
    op.drop_column('users', 'birthdate')
    op.create_unique_constraint('forgot_password_identifier_key', 'forgot_password', ['identifier'])
    # ### end Alembic commands ###
