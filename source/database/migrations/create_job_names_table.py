MIGRATION_NAME = "create_job_names_table"

'''
Migration script to create the job_names table
'''

def run_migration(database, logger):
    '''Run the migration to create the job_names table'''
    
    try:
        logger.info("Starting migration: Creating job_names table")
        
        database = database
        
        with database.atomic():
            cursor = database.execute_sql('''
                SELECT EXISTS (
                   SELECT 1 FROM information_schema.tables 
                   WHERE table_schema = 'public'
                   AND table_name = 'job_names'
                );
            ''')
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                logger.info("Creating job_names table...")
                database.execute_sql('''
                    CREATE TABLE job_names (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )
                ''')
                logger.info("job_names table created successfully")
            else:
                logger.info("job_names table already exists, skipping creation")
            
            # Insert predefined job names if they don't exist
            logger.info("Inserting predefined job names...")
            job_names = [
                "Corn Premerge",
                "Soybean Premerge",
                "Spring Burndown",
                "Rye Burndown",
                "Fall Burndown",
                "Corn Post V4-V6",
                "Corn R-1 Foliar",
                "Fungicide",
                "Spring Micros",
                "N-Sidedress #1",
                "N-Sidedress #2",
                "Hay Weed Cleanup"
            ]
            
            for job_name in job_names:
                # Check if job name already exists
                cursor = database.execute_sql(
                    "SELECT 1 FROM job_names WHERE name = ? LIMIT 1",
                    (job_name,)
                )
                if not cursor.fetchone():
                    # Job name doesn't exist, insert it
                    database.execute_sql(
                        "INSERT INTO job_names (name) VALUES (?)",
                        (job_name,)
                    )
            
            logger.info("Job names insertion completed")
        
        logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        return False