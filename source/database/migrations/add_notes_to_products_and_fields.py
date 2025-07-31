MIGRATION_NAME = "add_notes_to_products_and_fields"

'''Migration script to add notes column to products and fields'''

def run_migration(database, logger):
    '''Run the migration to add notes column to products and fields'''
    try:
        logger.info("Starting migration: add notes column to products and fields")
        with database.atomic():
            cursor = database.execute_sql("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'products'
                    AND column_name = 'notes'
                );
            """)
            product_notes_exists = cursor.fetchone()[0]
            if not product_notes_exists:
                database.execute_sql("ALTER TABLE products ADD COLUMN notes TEXT")
                logger.info("Added notes column to products table")
            
            cursor = database.execute_sql("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = 'fields'
                    AND column_name = 'notes'
                );
            """)
            field_notes_exists = cursor.fetchone()[0]
            if not field_notes_exists:
                database.execute_sql("ALTER TABLE fields ADD COLUMN notes TEXT")
                logger.info("Added notes column to fields table")
        
        logger.info("Migration completed")
        return True
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 