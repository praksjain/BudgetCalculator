"""Change user role from enum to string

Revision ID: 003
Revises: 6ced8644e8db
Create Date: 2025-06-09 06:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '6ced8644e8db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change role column from enum to string
    op.alter_column('users', 'role',
                   type_=sa.String(),
                   nullable=False,
                   server_default='project_manager',
                   postgresql_using='role::text')
    
    # Drop the enum type if it exists
    conn = op.get_bind()
    conn.execute(sa.text("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                DROP TYPE userrole CASCADE;
            END IF;
        EXCEPTION
            WHEN others THEN
                NULL;
        END
        $$;
    """))


def downgrade() -> None:
    # Recreate enum type
    conn = op.get_bind()
    conn.execute(sa.text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                CREATE TYPE userrole AS ENUM ('director', 'delivery_manager', 'project_manager', 'custom');
            END IF;
        EXCEPTION
            WHEN duplicate_object THEN
                NULL;
        END
        $$;
    """))
    
    # Change role column back to enum
    op.alter_column('users', 'role',
                   type_=postgresql.ENUM('director', 'delivery_manager', 'project_manager', 'custom', name='userrole'),
                   nullable=False,
                   postgresql_using='role::userrole') 