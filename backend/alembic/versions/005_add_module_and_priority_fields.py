"""Add module and priority fields

Revision ID: 005
Revises: 004
Create Date: 2025-06-09 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add module column to analysis_tasks
    op.add_column('analysis_tasks', sa.Column('module', sa.String(100), nullable=True))
    
    # Add priority column to analysis_subtasks
    op.add_column('analysis_subtasks', sa.Column('priority', sa.String(20), nullable=True, default='medium'))


def downgrade() -> None:
    # Remove module column from analysis_tasks
    op.drop_column('analysis_tasks', 'module')
    
    # Remove priority column from analysis_subtasks
    op.drop_column('analysis_subtasks', 'priority') 