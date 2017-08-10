"""create snippet table

Revision ID: 503f4485af7c
Revises:
Create Date: 2017-08-08 10:25:49.100041

"""

# revision identifiers, used by Alembic.
revision = '503f4485af7c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'snippet',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('desktop_redirect', sa.String, nullable=False),
        sa.Column('desktop_redirect_count', sa.Integer, default=0),
        sa.Column('mobile_redirect', sa.String),
        sa.Column('mobile_redirect_count', sa.Integer, default=0),
        sa.Column('tablet_redirect', sa.String),
        sa.Column('tablet_redirect_count', sa.Integer, default=0),
        sa.Column('short_url', sa.String),

        sa.Column(
            'created_at',
            sa.DateTime,
            nullable=False,
            server_default=sa.text('now()'),
            default=sa.text('now()')
        ),
        sa.Column('deleted_at', sa.DateTime),
        sa.Column(
            'updated_at', sa.DateTime, nullable=False,
            server_onupdate=sa.text('now()'),
            onupdate=sa.text('now()'),
            default=sa.text('now()')
        ),
    )


def downgrade():
    op.drop_table('snippet')
