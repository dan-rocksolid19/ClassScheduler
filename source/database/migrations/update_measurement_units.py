MIGRATION_NAME = "update_measurement_units"

'''
Migration script to update volume_units table to measurement_units
and add unit_type column for distinguishing between volume and weight units.

This migration:
1. Creates new measurement_units table
2. Migrates existing volume units data
3. Updates conversion factors to use new base units
4. Drops old volume_units table
'''

def run_migration(database, logger):
    """
    Run the migration to update volume_units to measurement_units
    """
    try:
        db = database
        logger.info("Starting migration: Update volume_units to measurement_units")
        
        with db.atomic():
            cursor = db.execute_sql('''
                SELECT EXISTS (
                   SELECT 1 FROM information_schema.tables 
                   WHERE table_schema = 'public'
                   AND table_name = 'measurement_units'
                );
            ''')
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                logger.info("Creating measurement_units table...")
                
                # Create new measurement_units table
                db.execute_sql('''
                    CREATE TABLE measurement_units (
                        id SERIAL PRIMARY KEY,
                        symbol TEXT NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        base_unit TEXT NOT NULL,
                        conversion_factor FLOAT NOT NULL,
                        is_system BOOLEAN DEFAULT FALSE,
                        is_selected BOOLEAN DEFAULT FALSE,
                        display_order INTEGER DEFAULT 0,
                        unit_type TEXT NOT NULL DEFAULT 'volume'
                    )
                ''')
                
                # Create index on unit_type
                db.execute_sql('''
                    CREATE INDEX idx_measurement_units_unit_type 
                    ON measurement_units(unit_type)
                ''')
                
                logger.info("measurement_units table created successfully")
                
                # Migrate existing volume units data
                logger.info("Migrating existing volume units data...")
                db.execute_sql('''
                    INSERT INTO measurement_units (
                        id, symbol, name, base_unit, conversion_factor,
                        is_system, is_selected, display_order, unit_type
                    )
                    SELECT 
                        id, symbol, name, 'fl oz', 
                        CASE 
                            WHEN symbol = 'tsp' THEN 1.0/6.0
                            WHEN symbol = 'tbsp' THEN 1.0/2.0
                            WHEN symbol = 'fl oz' THEN 1.0
                            WHEN symbol = 'cup' THEN 8.0
                            WHEN symbol = 'pt' THEN 16.0
                            WHEN symbol = 'qt' THEN 32.0
                            WHEN symbol = 'gal' THEN 128.0
                            ELSE conversion_factor
                        END,
                        is_system, is_selected, display_order, 'volume'
                    FROM volume_units
                ''')
                
                # Insert default weight units
                logger.info("Inserting default weight units...")
                weight_units = [
                    ('oz', 'Ounce', 'oz', 1.0, True, True, 0),
                    ('lb', 'Pound', 'oz', 16.0, True, True, 1),
                    ('ton', 'Short Ton', 'oz', 32000.0, True, True, 2)
                ]
                
                for symbol, name, base_unit, factor, is_system, is_selected, display_order in weight_units:
                    db.execute_sql('''
                        INSERT INTO measurement_units (
                            symbol, name, base_unit, conversion_factor,
                            is_system, is_selected, display_order, unit_type
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'weight')
                    ''', (symbol, name, base_unit, factor, is_system, is_selected, display_order))
                
                # Drop old volume_units table
                logger.info("Dropping old volume_units table...")
                db.execute_sql('DROP TABLE volume_units')
                
                logger.info("Migration completed successfully")
            else:
                logger.info("measurement_units table already exists, skipping migration")
            
            return True
            
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False 