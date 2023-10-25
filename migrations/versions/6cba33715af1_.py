"""empty message

Revision ID: 6cba33715af1
Revises: ff5f4b2d6cc1
Create Date: 2023-10-25 22:04:24.233847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cba33715af1'
down_revision = 'ff5f4b2d6cc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('climate',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('climate',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
