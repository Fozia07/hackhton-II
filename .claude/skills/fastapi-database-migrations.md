# FastAPI Database Migrations with Alembic

## Expertise
Expert skill for managing database schema migrations in FastAPI applications using Alembic. Specializes in migration creation, version control, rollback strategies, and production-safe database changes with SQLModel/SQLAlchemy integration.

## Purpose
This skill handles database migration concerns, enabling you to:
- Initialize Alembic for FastAPI projects
- Generate migrations from SQLModel model changes
- Apply and rollback migrations safely
- Manage migration history and branching
- Handle data migrations alongside schema changes
- Deploy migrations in production environments
- Resolve migration conflicts
- Test migrations before deployment

## When to Use
Use this skill when you need to:
- Set up database migrations for a new FastAPI project
- Create migrations for model changes (add/modify/delete columns, tables)
- Apply migrations to development, staging, or production databases
- Rollback problematic migrations
- Migrate data during schema changes
- Handle multiple database branches or environments
- Resolve migration conflicts in team environments
- Automate migrations in CI/CD pipelines

## Core Concepts

### 1. Alembic Installation and Setup

**Install Alembic**:
```bash
# Install Alembic
pip install alembic

# For async support
pip install alembic[asyncio]

# Install database drivers
pip install psycopg2-binary  # PostgreSQL
pip install asyncpg  # Async PostgreSQL
pip install aiomysql  # Async MySQL
```

**Initialize Alembic**:
```bash
# Initialize Alembic in your project
alembic init alembic

# This creates:
# alembic/
#   ├── env.py           # Migration environment configuration
#   ├── script.py.mako   # Migration template
#   ├── README
#   └── versions/        # Migration files directory
# alembic.ini            # Alembic configuration file
```

### 2. Alembic Configuration

**alembic.ini Configuration**:
```ini
# alembic.ini
[alembic]
# Path to migration scripts
script_location = alembic

# Template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s

# Timezone for migration timestamps
timezone = UTC

# Database URL (can be overridden by env.py)
# sqlalchemy.url = postgresql://user:pass@localhost/dbname

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**env.py Configuration for SQLModel**:
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.config import get_settings
from sqlmodel import SQLModel

# Import all models to ensure they're registered
from models.user import User
from models.post import Post
from models.comment import Comment
# Import all other models...

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = SQLModel.metadata

# Get database URL from settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    Creates an Engine and associates a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**env.py for Async SQLModel**:
```python
# alembic/env.py (async version)
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.config import get_settings
from sqlmodel import SQLModel

# Import all models
from models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run migrations with connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

### 3. Creating Migrations

**Auto-generate Migration from Model Changes**:
```bash
# Generate migration automatically by comparing models to database
alembic revision --autogenerate -m "Add user table"

# This creates a file like:
# alembic/versions/20260107_1430_abc123_add_user_table.py
```

**Manual Migration Creation**:
```bash
# Create empty migration file for manual editing
alembic revision -m "Add custom index"
```

**Example Auto-generated Migration**:
```python
# alembic/versions/20260107_1430_abc123_add_user_table.py
"""Add user table

Revision ID: abc123
Revises:
Create Date: 2026-01-07 14:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers
revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)


def downgrade() -> None:
    """Downgrade database schema."""
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
```

**Migration for Adding Column**:
```python
"""Add user role column

Revision ID: def456
Revises: abc123
Create Date: 2026-01-07 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'def456'
down_revision = 'abc123'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add role column to user table."""
    op.add_column('user', sa.Column('role', sa.String(length=50), nullable=True))

    # Set default value for existing rows
    op.execute("UPDATE user SET role = 'user' WHERE role IS NULL")

    # Make column non-nullable after setting defaults
    op.alter_column('user', 'role', nullable=False)


def downgrade() -> None:
    """Remove role column from user table."""
    op.drop_column('user', 'role')
```

**Migration for Modifying Column**:
```python
"""Change email column length

Revision ID: ghi789
Revises: def456
Create Date: 2026-01-07 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'ghi789'
down_revision = 'def456'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Increase email column length."""
    op.alter_column(
        'user',
        'email',
        type_=sa.String(length=255),
        existing_type=sa.String(length=100),
        nullable=False
    )


def downgrade() -> None:
    """Revert email column length."""
    op.alter_column(
        'user',
        'email',
        type_=sa.String(length=100),
        existing_type=sa.String(length=255),
        nullable=False
    )
```

### 4. Applying and Rolling Back Migrations

**Apply Migrations**:
```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade by specific number of revisions
alembic upgrade +1
alembic upgrade +2

# Upgrade to specific revision
alembic upgrade abc123

# Show SQL without executing
alembic upgrade head --sql
```

**Rollback Migrations**:
```bash
# Downgrade by one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade abc123

# Downgrade to base (remove all migrations)
alembic downgrade base

# Show SQL without executing
alembic downgrade -1 --sql
```

**Check Current Version**:
```bash
# Show current database version
alembic current

# Show migration history
alembic history

# Show verbose history with details
alembic history --verbose

# Show pending migrations
alembic history --indicate-current
```

### 5. Data Migrations

**Migration with Data Transformation**:
```python
"""Split name into first_name and last_name

Revision ID: jkl012
Revises: ghi789
Create Date: 2026-01-07 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'jkl012'
down_revision = 'ghi789'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Split name column into first_name and last_name."""
    # Add new columns
    op.add_column('user', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=100), nullable=True))

    # Migrate data
    connection = op.get_bind()
    users = connection.execute(sa.text("SELECT id, name FROM user")).fetchall()

    for user_id, name in users:
        if name:
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

            connection.execute(
                sa.text("UPDATE user SET first_name = :first, last_name = :last WHERE id = :id"),
                {"first": first_name, "last": last_name, "id": user_id}
            )

    # Make columns non-nullable
    op.alter_column('user', 'first_name', nullable=False)
    op.alter_column('user', 'last_name', nullable=False)

    # Drop old column
    op.drop_column('user', 'name')


def downgrade() -> None:
    """Combine first_name and last_name back into name."""
    # Add name column back
    op.add_column('user', sa.Column('name', sa.String(length=200), nullable=True))

    # Migrate data back
    connection = op.get_bind()
    users = connection.execute(
        sa.text("SELECT id, first_name, last_name FROM user")
    ).fetchall()

    for user_id, first_name, last_name in users:
        name = f"{first_name} {last_name}".strip()
        connection.execute(
            sa.text("UPDATE user SET name = :name WHERE id = :id"),
            {"name": name, "id": user_id}
        )

    # Make column non-nullable
    op.alter_column('user', 'name', nullable=False)

    # Drop new columns
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
```

**Bulk Data Migration**:
```python
"""Populate default categories

Revision ID: mno345
Revises: jkl012
Create Date: 2026-01-07 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = 'mno345'
down_revision = 'jkl012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Insert default categories."""
    categories_table = sa.table(
        'category',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('slug', sa.String),
        sa.column('created_at', sa.DateTime)
    )

    op.bulk_insert(
        categories_table,
        [
            {'name': 'Technology', 'slug': 'technology', 'created_at': datetime.utcnow()},
            {'name': 'Science', 'slug': 'science', 'created_at': datetime.utcnow()},
            {'name': 'Business', 'slug': 'business', 'created_at': datetime.utcnow()},
        ]
    )


def downgrade() -> None:
    """Remove default categories."""
    op.execute("DELETE FROM category WHERE slug IN ('technology', 'science', 'business')")
```

### 6. Advanced Migration Patterns

**Migration with Foreign Key**:
```python
"""Add posts table with user foreign key

Revision ID: pqr678
Revises: mno345
Create Date: 2026-01-07 17:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'pqr678'
down_revision = 'mno345'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create posts table with foreign key to users."""
    op.create_table(
        'post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_user_id'), 'post', ['user_id'], unique=False)


def downgrade() -> None:
    """Drop posts table."""
    op.drop_index(op.f('ix_post_user_id'), table_name='post')
    op.drop_table('post')
```

**Migration with Enum Type**:
```python
"""Add status enum to posts

Revision ID: stu901
Revises: pqr678
Create Date: 2026-01-07 17:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'stu901'
down_revision = 'pqr678'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add status column with enum type."""
    # For PostgreSQL
    status_enum = sa.Enum('draft', 'published', 'archived', name='post_status')
    status_enum.create(op.get_bind())

    op.add_column('post', sa.Column('status', status_enum, nullable=True))
    op.execute("UPDATE post SET status = 'published' WHERE status IS NULL")
    op.alter_column('post', 'status', nullable=False)


def downgrade() -> None:
    """Remove status column and enum type."""
    op.drop_column('post', 'status')

    # For PostgreSQL
    sa.Enum(name='post_status').drop(op.get_bind())
```

**Migration with Index**:
```python
"""Add composite index for user posts

Revision ID: vwx234
Revises: stu901
Create Date: 2026-01-07 18:00:00.000000
"""
from alembic import op

revision = 'vwx234'
down_revision = 'stu901'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add composite index on user_id and created_at."""
    op.create_index(
        'ix_post_user_created',
        'post',
        ['user_id', 'created_at'],
        unique=False
    )


def downgrade() -> None:
    """Remove composite index."""
    op.drop_index('ix_post_user_created', table_name='post')
```

### 7. Testing Migrations

**Migration Test Setup**:
```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel

@pytest.fixture
def alembic_config():
    """Create Alembic configuration for testing."""
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
    return config

def test_migrations_up_and_down(alembic_config):
    """Test that migrations can be applied and rolled back."""
    # Upgrade to head
    command.upgrade(alembic_config, "head")

    # Verify tables exist
    engine = create_engine(alembic_config.get_main_option("sqlalchemy.url"))
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        assert 'user' in tables
        assert 'post' in tables

    # Downgrade to base
    command.downgrade(alembic_config, "base")

    # Verify tables are removed
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        assert 'user' not in tables
        assert 'post' not in tables

def test_migration_data_integrity(alembic_config):
    """Test that data migrations preserve data correctly."""
    engine = create_engine(alembic_config.get_main_option("sqlalchemy.url"))

    # Apply migrations up to before data migration
    command.upgrade(alembic_config, "jkl012-1")

    # Insert test data
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO user (name) VALUES ('John Doe')"))
        conn.commit()

    # Apply data migration
    command.upgrade(alembic_config, "jkl012")

    # Verify data was migrated correctly
    with engine.connect() as conn:
        result = conn.execute(text("SELECT first_name, last_name FROM user")).fetchone()
        assert result[0] == 'John'
        assert result[1] == 'Doe'
```

### 8. Production Deployment

**Pre-deployment Checklist**:
```python
# scripts/check_migrations.py
"""
Check migrations before deployment.
"""
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from core.config import get_settings

def check_migrations():
    """Check migration status and safety."""
    settings = get_settings()
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.database_url)

    # Get current database version
    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()

    # Get head version
    script = ScriptDirectory.from_config(config)
    head_rev = script.get_current_head()

    print(f"Current database version: {current_rev}")
    print(f"Latest migration version: {head_rev}")

    if current_rev == head_rev:
        print("✓ Database is up to date")
        return True
    else:
        print("⚠ Database needs migration")

        # Show pending migrations
        print("\nPending migrations:")
        for rev in script.iterate_revisions(current_rev, head_rev):
            print(f"  - {rev.revision}: {rev.doc}")

        return False

if __name__ == "__main__":
    check_migrations()
```

**Deployment Script**:
```bash
#!/bin/bash
# scripts/deploy_migrations.sh

set -e  # Exit on error

echo "Starting migration deployment..."

# Backup database
echo "Creating database backup..."
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Check current migration status
echo "Checking migration status..."
python scripts/check_migrations.py

# Run migrations
echo "Applying migrations..."
alembic upgrade head

# Verify migrations
echo "Verifying migrations..."
alembic current

echo "Migration deployment complete!"
```

**Zero-Downtime Migration Strategy**:
```python
"""
Zero-downtime migration example: Adding a non-nullable column

Step 1: Add column as nullable
Step 2: Deploy code that writes to new column
Step 3: Backfill existing rows
Step 4: Make column non-nullable
"""

# Migration 1: Add nullable column
def upgrade_step1():
    op.add_column('user', sa.Column('phone', sa.String(20), nullable=True))

# Migration 2: Backfill data (run after code deployment)
def upgrade_step2():
    op.execute("UPDATE user SET phone = '' WHERE phone IS NULL")

# Migration 3: Make non-nullable
def upgrade_step3():
    op.alter_column('user', 'phone', nullable=False)
```

## Best Practices

### 1. Migration Creation
- Always review auto-generated migrations
- Test migrations on development database first
- Write both upgrade and downgrade functions
- Keep migrations small and focused
- Add descriptive migration messages

### 2. Data Safety
- Always backup database before migrations
- Test rollback procedures
- Use transactions for data migrations
- Validate data after migrations
- Consider zero-downtime strategies for production

### 3. Team Collaboration
- Commit migrations to version control
- Resolve migration conflicts promptly
- Communicate breaking changes
- Document complex migrations
- Use consistent naming conventions

### 4. Production Considerations
- Run migrations during maintenance windows
- Monitor migration execution time
- Have rollback plan ready
- Test migrations on staging first
- Use database replicas for validation

### 5. Performance
- Create indexes in separate migrations
- Use batch operations for large data migrations
- Consider migration execution time
- Avoid locking tables during peak hours
- Use concurrent index creation when possible

## Common Issues and Solutions

### Issue: Migration Conflicts
```bash
# When multiple developers create migrations
# Solution: Merge migrations or create merge migration
alembic merge -m "Merge migrations" rev1 rev2
```

### Issue: Failed Migration
```bash
# Mark migration as complete without running
alembic stamp head

# Or rollback and fix
alembic downgrade -1
# Fix migration file
alembic upgrade head
```

### Issue: Out of Sync Database
```bash
# Generate migration from current database state
alembic revision --autogenerate -m "Sync database"
# Review and apply
```

## Summary

This skill provides comprehensive guidance for managing database migrations in FastAPI applications with:
- Alembic setup and configuration for SQLModel
- Migration creation (auto-generate and manual)
- Schema migrations (tables, columns, indexes, foreign keys)
- Data migrations with transformation logic
- Testing strategies for migrations
- Production deployment patterns
- Zero-downtime migration strategies
- Best practices for team collaboration and safety

Use this skill to ensure your FastAPI applications have robust, version-controlled database schema management with safe migration and rollback capabilities for production environments.
