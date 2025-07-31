'''
These functions and variables are made available by LibrePy
Check out the help manual for a full list

createUnoService()      # Implementation of the Basic CreateUnoService command
getUserPath()          # Get the user path of the currently running instance
thisComponent          # Current component instance
getDefaultContext()    # Get the default context
MsgBox()               # Simple msgbox that takes the same arguments as the Basic MsgBox
mri(obj)               # Mri the object. MRI must be installed for this to work
doc_object             # A generic object with a dict_values and list_values that are persistent

To import files inside this project, use the 'librepy' keyword
For example, to import a file named config, use the following:
from librepy import config
'''

from librepy.model.fertilizer_cmd_ctr import (
        Category, Subcategory, 
        JobName, Product, Field, BusinessInfo, MeasurementUnit,
        Job, JobWeather, JobField, JobBatch, JobProduct, JobBatchProduct
    )

# Models that should be created directly (not via migrations)
# FertilizerCmdCtrSettings is handled by migration to avoid index conflicts
REQUIRED_MODELS = [
        Category, Subcategory, JobName, 
        Product, Field, BusinessInfo, MeasurementUnit, Job, 
        JobWeather, JobField, JobBatch, JobProduct, JobBatchProduct
    ]

def verify_and_create_tables(logger, database):
    """
    Verify if all required tables exist in the database and create them if needed
    Returns tuple of (success, message)
    """
    try:
        try:
            models = REQUIRED_MODELS
            logger.debug(f"Loaded {len(models)} models for table verification")
        except Exception as e:
            logger.error(f"Failed to initialize models: {str(e)}")
            return False, f"Could not initialize database models: {str(e)}"
        
        # Check if tables exist and create them if they don't
        created_tables = []
        failed_tables = []
        
        for model in models:
            try:
                logger.debug(f"Checking if table exists: {model._meta.table_name}")
                table_exists = database.table_exists(model._meta.table_name)
                logger.debug(f"Table {model._meta.table_name} exists: {table_exists}")
                
                if not table_exists:
                    logger.debug(f"Creating table: {model._meta.table_name}")
                    logger.debug(f"Model database instance: {model._meta.database}")
                    logger.debug(f"Expected database instance: {database}")
                    
                    try:
                        # Use safe=True to create table with IF NOT EXISTS
                        model.create_table(safe=True)
                        created_tables.append(model._meta.table_name)
                        logger.info(f"Created table: {model._meta.table_name}")
                    except Exception as create_error:
                        error_msg = str(create_error).lower()
                        # Check if error is about something already existing (table, index, constraint)
                        if any(keyword in error_msg for keyword in ['already exists', 'duplicate', 'exists']):
                            logger.warning(f"Table {model._meta.table_name} or its components already exist, treating as success: {str(create_error)}")
                            # This is acceptable - table exists, possibly from previous partial creation
                        else:
                            # This is a real error we should report
                            raise create_error
                            
            except Exception as e:
                failed_tables.append(f"{model._meta.table_name}: {str(e)}")
                logger.error(f"Failed to create table {model._meta.table_name}: {str(e)}")
        
        if failed_tables:
            return False, f"Failed to create the following tables: {', '.join(failed_tables)}"
        
        if created_tables:
            message = f"Successfully created {len(created_tables)} tables: {', '.join(created_tables)}"
        else:
            message = "All required tables already exist"
            
        return True, message
        
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        return False, f"Unexpected error during table verification: {str(e)}"

def initialize_database(logger, database):
    """
    Initialize the database with required tables and default data
    Returns tuple of (success, message)
    """
    success, message = verify_and_create_tables(logger, database)
    if not success:
        database.close()
        return False, f"Table creation failed: {message}"
    
    try:
        from librepy.fertilizer_cmd_ctr.data.business_info_dao import BusinessInfoDAO
        business_info_dao = BusinessInfoDAO(logger)
        if not business_info_dao.ensure_business_info_exists():
            return False, "Failed to initialize business info: Could not create or verify business information table"
    except Exception as e:
        database.close()
        logger.error(f"Business info initialization error: {str(e)}")
        return False, f"Business info initialization failed: {str(e)}"
    
    try:
        from librepy.fertilizer_cmd_ctr.data.category_dao import CategoryDAO
        category_dao = CategoryDAO(logger)
        success, message = category_dao.initialize_default_categories()
        if not success:
            return False, f"Category initialization failed: {message}"
    except Exception as e:
        database.close()
        logger.error(f"Category initialization error: {str(e)}")
        return False, f"Category initialization failed: {str(e)}"
    
    try:
        from librepy.fertilizer_cmd_ctr.data.measurement_unit_dao import MeasurementUnitDAO
        measurement_unit_dao = MeasurementUnitDAO(logger)
        success, message = measurement_unit_dao.initialize_default_units()
        if not success:
            return False, f"Default measurement units initialization failed: {message}"
    except Exception as e:
        database.close()
        logger.error(f"Measurement unit initialization error: {str(e)}")
        return False, f"Default measurement units initialization failed: {str(e)}"
    
    return True, "Database initialized successfully"