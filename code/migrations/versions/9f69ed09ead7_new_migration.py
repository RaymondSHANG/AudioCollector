"""new migration

Revision ID: 9f69ed09ead7
Revises: 
Create Date: 2024-04-21 21:15:49.665139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f69ed09ead7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    sa.Column('hashtags', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('given_name', sa.String(length=64), nullable=True),
    sa.Column('family_name', sa.String(length=64), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('identifier_system', sa.String(), nullable=True),
    sa.Column('identifier_value', sa.String(length=64), nullable=True),
    sa.Column('oauth_server', sa.String(length=64), nullable=True),
    sa.Column('idx_patient_id', sa.Integer(), nullable=True),
    sa.Column('idx_user_email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_idx_patient_id'), ['idx_patient_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_idx_user_email'), ['idx_user_email'], unique=True)

    op.create_table('audio_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('news_id', sa.Integer(), nullable=False),
    sa.Column('record_date', sa.DateTime(), nullable=False),
    sa.Column('file_dir', sa.String(length=255), nullable=False),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], name='fk_audio_record_news_id'),
    sa.ForeignKeyConstraint(['patient_id'], ['users.id'], name='fk_audio_record_user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('audio_records')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_idx_user_email'))
        batch_op.drop_index(batch_op.f('ix_users_idx_patient_id'))

    op.drop_table('users')
    op.drop_table('news')
    # ### end Alembic commands ###
