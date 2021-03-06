"""empty message

Revision ID: 95e7ab6c0e3a
Revises: 
Create Date: 2020-07-09 22:06:07.398879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95e7ab6c0e3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('_password', sa.String(length=256), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('is_super', sa.Boolean(), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('letter',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('letter', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('letter')
    )
    op.create_table('movie_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('_password', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=32), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('showname', sa.String(length=64), nullable=True),
    sa.Column('shownameen', sa.String(length=128), nullable=True),
    sa.Column('director', sa.String(length=64), nullable=True),
    sa.Column('leadingRole', sa.String(length=256), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('language', sa.String(length=64), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('screeningmodel', sa.String(length=32), nullable=True),
    sa.Column('openday', sa.DateTime(), nullable=True),
    sa.Column('backgroundpicture', sa.String(length=256), nullable=True),
    sa.Column('flag', sa.Boolean(), nullable=True),
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('letter_id', sa.Integer(), nullable=True),
    sa.Column('c_id', sa.Integer(), nullable=True),
    sa.Column('c_parent_id', sa.Integer(), nullable=True),
    sa.Column('c_region_name', sa.String(length=16), nullable=True),
    sa.Column('c_city_code', sa.Integer(), nullable=True),
    sa.Column('c_pinyin', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['letter_id'], ['letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city')
    op.drop_table('movies')
    op.drop_table('movie_user')
    op.drop_table('letter')
    op.drop_table('admin_user')
    # ### end Alembic commands ###
