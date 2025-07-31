from librepy.model.db_connection import get_database_connection
from librepy.database.migrations import make_subcategory_optional
from librepy.database.migrations import create_job_names_table
from librepy.database.migrations import update_measurement_units
from librepy.database.migrations import add_gallons_to_batch_products
from librepy.database.migrations import add_rate_basis_to_products
from librepy.database.migrations import add_rate_basis_to_job_products
from librepy.database.migrations import add_notes_to_products_and_fields
from librepy.database.migrations import create_fertilizer_settings_table

MIGRATION_ORDER = [
    ('create_fertilizer_settings_table', create_fertilizer_settings_table),
    ('make_subcategory_optional', make_subcategory_optional),
    ('create_job_names_table', create_job_names_table),
    ('update_measurement_units', update_measurement_units),
    ('add_gallons_to_batch_products', add_gallons_to_batch_products),
    ('add_rate_basis_to_products', add_rate_basis_to_products),
    ('add_rate_basis_to_job_products', add_rate_basis_to_job_products),
    ('add_notes_to_products_and_fields', add_notes_to_products_and_fields),
]

def _ensure_schema_migrations_table(database, logger):
    """Create the schema_migrations table if it doesn't exist"""
    try:
        with database.atomic():
            cursor = database.execute_sql("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'schema_migrations'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                database.execute_sql("""
                    CREATE TABLE schema_migrations (
                        id SERIAL PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        applied_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                logger.info("Created schema_migrations table")
            else:
                logger.debug("schema_migrations table already exists")
        
        return True
    except Exception as e:
        logger.error(f"Failed to create schema_migrations table: {str(e)}")
        return False

def _is_migration_applied(database, migration_name):
    """Check if a migration has already been applied"""
    try:
        cursor = database.execute_sql(
            "SELECT 1 FROM schema_migrations WHERE name = ? LIMIT 1",
            (migration_name,)
        )
        return cursor.fetchone() is not None
    except Exception:
        return False

def _record_migration(database, migration_name, logger):
    """Record that a migration has been applied"""
    try:
        database.execute_sql(
            "INSERT INTO schema_migrations (name) VALUES (?)",
            (migration_name,)
        )
        logger.info(f"Recorded migration: {migration_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to record migration {migration_name}: {str(e)}")
        return False

def run_all_migrations(logger, database=None):
    """
    Run all migrations that haven't been applied yet on the supplied database (or default connection).
    Returns True if all migrations succeeded, False otherwise.
    """
    try:
        logger.info("Starting automatic migration process")
        
        # Use provided database or fall back to default connection
        if database is None:
            logger.debug("Getting default database connection")
            database = get_database_connection()
            close_db = True
        else:
            logger.debug("Using provided database connection")
            close_db = False
        
        if not database:
            logger.error("Could not get database connection for migrations")
            MsgBox("Database migration failed: Could not connect to database", 16, "Migration Error")
            return False
        
        logger.debug(f"Database instance created: {type(database).__name__}")
        logger.debug(f"Database connection state before connect(): {database.is_connection_usable()}")
        
        database.connect()
        
        logger.debug(f"Database connection state after connect(): {database.is_connection_usable()}")
        logger.info("Database connection established successfully")
        
        # Ensure models are properly bound to this database instance
        logger.debug("Ensuring models are bound to database connection")
        from librepy.model.db_connection import _bind_models_to_db
        _bind_models_to_db(database)
        
        # Ensure core tables exist before migrations
        from librepy.model.db_init import initialize_database
        logger.debug("Starting database initialization")
        init_success, init_msg = initialize_database(logger, database)
        if not init_success:
            logger.error(f"Database initialization failed: {init_msg}")
            if close_db:
                database.close()
            MsgBox(f"Database initialization failed: {init_msg}", 16, "Migration Error")
            return False
        logger.info("Database initialization completed successfully")
        
        if not _ensure_schema_migrations_table(database, logger):
            database.close()
            MsgBox("Database migration failed: Could not create tracking table", 16, "Migration Error")
            return False
        
        migrations_run = 0
        migrations_skipped = 0
        
        for migration_name, migration_module in MIGRATION_ORDER:
            try:
                if _is_migration_applied(database, migration_name):
                    logger.debug(f"Skipping already applied migration: {migration_name}")
                    migrations_skipped += 1
                    continue
                
                logger.info(f"Running migration: {migration_name}")
                
                with database.atomic():
                    success = migration_module.run_migration(database, logger)
                    if not success:
                        logger.error(f"Migration {migration_name} failed")
                        MsgBox(f"Database migration failed: {migration_name}", 16, "Migration Error")
                        return False
                    
                    if not _record_migration(database, migration_name, logger):
                        logger.error(f"Failed to record migration {migration_name}")
                        MsgBox(f"Database migration failed: Could not record {migration_name}", 16, "Migration Error")
                        return False
                
                migrations_run += 1
                logger.info(f"Successfully completed migration: {migration_name}")
                
            except Exception as e:
                logger.error(f"Exception during migration {migration_name}: {str(e)}")
                MsgBox(f"Database migration failed: {migration_name} - {str(e)}", 16, "Migration Error")
                return False
        
        if close_db:
            database.close()
        
        if migrations_run > 0:
            logger.info(f"Migration process completed: {migrations_run} migrations applied, {migrations_skipped} skipped")
        else:
            logger.info(f"Migration process completed: All {migrations_skipped} migrations already applied")
        
        return True
        
    except Exception as e:
        logger.error(f"Migration process failed with exception: {str(e)}")
        MsgBox(f"Database migration failed: {str(e)}", 16, "Migration Error")
        return False 