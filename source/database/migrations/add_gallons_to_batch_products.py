MIGRATION_NAME = "add_gallons_to_batch_products"

'''
Migration script to add gallons column to job_batch_products table

This migration:
1. Adds a gallons column to the job_batch_products table
2. Calculates and populates gallons values for existing volume-based products
'''

def run_migration(database, logger):
    """
    Run the migration to add gallons column to job_batch_products table
    """
    try:
        db = database
        logger.info("Starting migration: Add gallons column to job_batch_products table")
        
        with db.atomic():
            # Check if gallons column already exists
            cursor = db.execute_sql('''
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_schema = 'public'
                    AND table_name = 'job_batch_products'
                    AND column_name = 'gallons'
                );
            ''')
            column_exists = cursor.fetchone()[0]
            
            if not column_exists:
                logger.info("Adding gallons column to job_batch_products table...")
                db.execute_sql("ALTER TABLE job_batch_products ADD COLUMN gallons DECIMAL(10,2) NULL")
                logger.info("Gallons column added successfully")
                
                # Update existing records to calculate gallons for volume products
                logger.info("Calculating gallons for existing volume-based products...")
                update_query = '''
                    UPDATE job_batch_products 
                    SET gallons = (
                        CASE 
                            WHEN mu.unit_type = 'volume' THEN 
                                ROUND(COALESCE(job_batch_products.amount * mu.conversion_factor / gal_conversion.conversion_factor, 0)::NUMERIC, 2)
                            ELSE NULL
                        END
                    )
                    FROM job_products jp
                    JOIN products p ON jp.product_id = p.id
                    JOIN measurement_units mu ON jp.rate_unit = mu.symbol
                    CROSS JOIN (SELECT conversion_factor FROM measurement_units WHERE symbol = 'gal' AND unit_type = 'volume') gal_conversion
                    WHERE job_batch_products.job_product_id = jp.id
                '''
                
                db.execute_sql(update_query)
                logger.info("Gallons calculation completed for existing records")
                
                # Verify the migration
                cursor = db.execute_sql('''
                    SELECT COUNT(*) as total_records, 
                           COUNT(gallons) as records_with_gallons,
                           COUNT(CASE WHEN gallons > 0 THEN 1 END) as records_with_positive_gallons
                    FROM job_batch_products
                ''')
                stats = cursor.fetchone()
                if stats:
                    total, with_gallons, positive_gallons = stats
                    logger.info(f"Migration verification: {total} total records, {with_gallons} with gallons data, {positive_gallons} with positive gallon values")
                
            else:
                logger.info("Gallons column already exists in job_batch_products table, skipping migration")
        
        logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 