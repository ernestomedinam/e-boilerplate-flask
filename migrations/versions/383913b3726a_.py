"""empty message

Revision ID: 383913b3726a
Revises: 
Create Date: 2021-05-21 05:54:23.399761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '383913b3726a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('parts', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mock')
    # ### end Alembic commands ###
