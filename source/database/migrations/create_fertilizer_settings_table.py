MIGRATION_NAME = "create_fertilizer_settings_table"

'''
Migration script to create the fertilizer_cmd_ctr_settings table with proper idempotent handling
'''

def run_migration(database, logger):
    '''Run the migration to create the fertilizer_cmd_ctr_settings table'''
    
    try:
        logger.info("Starting migration: Creating fertilizer_cmd_ctr_settings table")
        
        with database.atomic():
            cursor = database.execute_sql('''
                SELECT EXISTS (
                   SELECT 1 FROM information_schema.tables 
                   WHERE table_schema = 'public'
                   AND table_name = 'fertilizer_cmd_ctr_settings'
                );
            ''')
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                logger.info("Creating fertilizer_cmd_ctr_settings table...")
                database.execute_sql('''
                    CREATE TABLE fertilizer_cmd_ctr_settings (
                        id SERIAL PRIMARY KEY,
                        setting_key VARCHAR(255) NOT NULL,
                        setting_value TEXT
                    )
                ''')
                logger.info("fertilizer_cmd_ctr_settings table created successfully")
            else:
                logger.info("fertilizer_cmd_ctr_settings table already exists, skipping creation")
            
            # Create the unique index separately with IF NOT EXISTS
            logger.info("Creating unique index on setting_key...")
            # Check if the index already exists (compatible with PostgreSQL 9.3)
            cursor = database.execute_sql('''
                SELECT EXISTS (
                    SELECT 1 FROM pg_indexes 
                    WHERE schemaname = 'public' 
                    AND indexname = 'fertilizercmdctrsettings_setting_key'
                );
            ''')
            index_exists = cursor.fetchone()[0]

            if not index_exists:
                try:
                    database.execute_sql('''
                        CREATE UNIQUE INDEX fertilizercmdctrsettings_setting_key 
                        ON fertilizer_cmd_ctr_settings (setting_key)
                    ''')
                    logger.info("Unique index created successfully")
                except Exception as index_error:
                    # Handle race condition where index was created between the check and creation attempt
                    error_msg = str(index_error).lower()
                    if 'already exists' in error_msg or 'duplicate' in error_msg:
                        logger.info("Unique index already exists, continuing")
                    else:
                        raise index_error
            else:
                logger.info("Unique index already exists, skipping creation")
        
        logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 