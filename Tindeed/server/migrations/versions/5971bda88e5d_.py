"""empty message

Revision ID: 5971bda88e5d
Revises: 5fbe7410a0d1
Create Date: 2023-05-18 16:15:37.844434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5971bda88e5d'
down_revision = '5fbe7410a0d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.alter_column('camera',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False)
        batch_op.alter_column('lights',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False)
        batch_op.alter_column('audio',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False)
        batch_op.alter_column('props',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False)
        batch_op.alter_column('editing_software',
               existing_type=sa.VARCHAR(),
               type_=sa.Boolean(),
               nullable=False)

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('location',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.alter_column('editing_software',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('props',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('audio',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('lights',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('camera',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###