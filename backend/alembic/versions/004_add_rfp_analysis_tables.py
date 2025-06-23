"""Add RFP analysis tables

Revision ID: 004
Revises: 003
Create Date: 2025-06-09 06:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create rfp_analyses table
    op.create_table(
        'rfp_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rfp_id', sa.Integer(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('scope', sa.Text(), nullable=True),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('deliverables', sa.Text(), nullable=True),
        sa.Column('timeline', sa.String(255), nullable=True),
        sa.Column('complexity_level', sa.String(50), nullable=True),
        sa.Column('technology_stack', sa.Text(), nullable=True),
        sa.Column('risks', sa.Text(), nullable=True),
        sa.Column('total_estimated_hours', sa.Float(), nullable=True),
        sa.Column('total_estimated_cost', sa.Float(), nullable=True),
        sa.Column('confidence_level', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['rfp_id'], ['rfps.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rfp_id')
    )
    op.create_index(op.f('ix_rfp_analyses_id'), 'rfp_analyses', ['id'], unique=False)
    
    # Create analysis_tasks table
    op.create_table(
        'analysis_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('priority', sa.String(20), nullable=True),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('complexity', sa.String(20), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['rfp_analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_tasks_id'), 'analysis_tasks', ['id'], unique=False)
    
    # Create analysis_subtasks table
    op.create_table(
        'analysis_subtasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('is_critical', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['analysis_tasks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_subtasks_id'), 'analysis_subtasks', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_analysis_subtasks_id'), table_name='analysis_subtasks')
    op.drop_table('analysis_subtasks')
    op.drop_index(op.f('ix_analysis_tasks_id'), table_name='analysis_tasks')
    op.drop_table('analysis_tasks')
    op.drop_index(op.f('ix_rfp_analyses_id'), table_name='rfp_analyses')
    op.drop_table('rfp_analyses') 