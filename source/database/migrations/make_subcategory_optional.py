MIGRATION_NAME = "make_subcategory_optional"

'''
Migration script to make subcategory optional in products table

This migration:
1. Drops the existing unique index on (category, subcategory, name)
2. Alters the subcategory column to allow NULL values
'''

def run_migration(database, logger):
    """
    Run the migration to make subcategory optional in products table and remove unique index
    """
    try:
        db = database
        logger.info("Starting migration: Make subcategory optional and remove index in products table")
        
        with db.atomic():
            
            db.execute_sql("DROP INDEX IF EXISTS products_category_id_subcategory_id_name")
            
            db.execute_sql("ALTER TABLE products ALTER COLUMN subcategory_id DROP NOT NULL")
            
        logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 