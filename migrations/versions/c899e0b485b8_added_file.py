"""Added file

Revision ID: c899e0b485b8
Revises: 5a68c7f9de9b
Create Date: 2021-09-21 17:33:53.487494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c899e0b485b8'
down_revision = '5a68c7f9de9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('store_json',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('json_file', sa.Text(), nullable=True),
    sa.Column('mimetype', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('store_json')
    # ### end Alembic commands ###