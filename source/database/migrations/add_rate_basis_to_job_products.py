MIGRATION_NAME = "add_rate_basis_to_job_products"

'''Migration script to add rate_basis column to job_products table'''

def run_migration(database, logger):
    '''Run the migration to add rate_basis column to job_products'''
    try:
        logger.info("Starting migration: add rate_basis column to job_products")
        with database.atomic():
            cursor = database.execute_sql("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'job_products'
                    AND column_name = 'rate_basis'
                );
            """)
            column_exists = cursor.fetchone()[0]
            if not column_exists:
                database.execute_sql("ALTER TABLE job_products ADD COLUMN rate_basis VARCHAR(10) NOT NULL DEFAULT 'acre'")
        logger.info("Migration completed")
        return True
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 