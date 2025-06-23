"""update_analysis_text_fields

Revision ID: 8067c3e7ba04
Revises: 005
Create Date: 2025-06-12 09:34:33.186537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8067c3e7ba04'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change timeline column from VARCHAR(255) to TEXT to handle longer AI-generated content
    op.alter_column('rfp_analyses', 'timeline',
                   existing_type=sa.VARCHAR(length=255),
                   type_=sa.Text(),
                   existing_nullable=True)
    
    # Change complexity_level column from VARCHAR(50) to VARCHAR(100) for more flexibility
    op.alter_column('rfp_analyses', 'complexity_level',
                   existing_type=sa.VARCHAR(length=50),
                   type_=sa.VARCHAR(length=100),
                   existing_nullable=True)


def downgrade() -> None:
    # Revert timeline column back to VARCHAR(255)
    op.alter_column('rfp_analyses', 'timeline',
                   existing_type=sa.Text(),
                   type_=sa.VARCHAR(length=255),
                   existing_nullable=True)
    
    # Revert complexity_level column back to VARCHAR(50)
    op.alter_column('rfp_analyses', 'complexity_level',
                   existing_type=sa.VARCHAR(length=100),
                   type_=sa.VARCHAR(length=50),
                   existing_nullable=True) 