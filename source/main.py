'''
These functions and variables are made available by LibrePy
Check out the help manual for a full list

createUnoService()      # Implementation of the Basic CreateUnoService command
getUserPath()           # Get the user path of the currently running instance
thisComponent           # Current component instance
getDefaultContext()     # Get the default context
MsgBox()                # Simple msgbox that takes the same arguments as the Basic MsgBox
mri(obj)                # Mri the object. MRI must be installed for this to work
doc_object              # A generic object with a dict_values and list_values that are persistent

To import files inside this project, use the 'librepy' keyword
For example, to import a file named config, use the following:
from librepy import config
'''

import os
import sys
import traceback
import uno
import threading
import time
import logging
from librepy.pybrex.values import pybrex_logger
    
logger = pybrex_logger(__name__)

def main(*args): 
    ''' Main method that is run when start is clicked in librepy '''
    logger.info("Main method started")
    try:
        # Import this first to catch the potential exception
        from librepy.peewee.connection.db_dialog import DBCanceledException
        
        ctx = getDefaultContext()
        smgr = ctx.getServiceManager()

        # Check database configuration and run migrations
        from librepy.peewee.db_migrations.migration_manager import run_all_migrations
        migration_success = run_all_migrations(logger)
        if not migration_success:
            logger.error("Database migrations failed, aborting application startup")
            return
        
        from librepy.fertilizer_cmd_ctr import main
        logger.info("Initializing FertilizerCmdCtr")
        fertilizer_cmd_ctr = main.FertilizerCmdCtr(ctx, smgr)
        logger.info("FertilizerCmdCtr initialized successfully")
    except DBCanceledException as e:
        # Handle database cancellation gracefully
        logger.info(f"Database setup canceled by user: {str(e)}")
        # Don't show an error message - this is an expected path
        return
    except Exception as e:
        logger.error(f"Error in main method: {str(e)}")
        logger.error(traceback.format_exc())
        MsgBox(f"An error occurred while starting the application: {str(e)}")
    
myDocument = None
_document_close_ready = False

def startup(*args):
    logger.info("Startup method called")
    try:
        # Import this first to catch the potential exception
        from librepy.peewee.connection.db_dialog import DBCanceledException
        from librepy.fertilizer_cmd_ctr.main import FertilizerCmdCtr
        from librepy.jasper_report.jasper_report_manager import precopy_all_templates
        global myDocument, _document_close_ready
        
        myDocument = thisComponent
        precopy_all_templates()
        logger.info("Document reference saved")
        
        try:
            thisComponent.getCurrentController().getFrame().getContainerWindow().Visible = False
            logger.info("Document window hidden")
        except Exception as e:
            logger.error(f"Failed to hide document window: {str(e)}")
            logger.error(traceback.format_exc())
        
        # Check database configuration BEFORE starting background thread
        # This ensures the dialog shows in the main thread if needed
        logger.info("Checking database configuration")
        try:
            from librepy.peewee.connection.db_connection import get_database_connection
            database = get_database_connection()
            database.connect()
            database.close()
            logger.info("Database configuration verified successfully")
        except DBCanceledException as e:
            logger.info(f"Database setup canceled by user: {str(e)}")
            close_file()
            return
        except Exception as e:
            logger.error(f"Database configuration failed: {str(e)}")
            close_file()
            return
        
        # Get context and service manager
        ctx = getDefaultContext()
        smgr = ctx.getServiceManager()
        
        # Define a wrapper function that handles the main application logic
        def run_app():
            try:
                # Run database migrations (should work now since config is verified)
                from librepy.peewee.db_migrations.migration_manager import run_all_migrations
                migration_success = run_all_migrations(logger)
                if not migration_success:
                    logger.error("Database migrations failed, aborting application startup")
                    close_file()
                    return
                
                app = FertilizerCmdCtr(ctx, smgr)
                # Set the flag when initialization is complete
                global _document_close_ready
                _document_close_ready = True
                # Close the document once we're ready
                close_file()
            except Exception as e:
                logger.error(f"Error in application thread: {str(e)}")
                logger.error(traceback.format_exc())
                close_file()
                
        # Start main application in a thread
        logger.info("Starting FertilizerCmdCtr in a new thread")
        threading.Thread(target=run_app).start()
        
    except DBCanceledException as e:
        # Handle database cancellation gracefully
        logger.info(f"Database setup canceled by user: {str(e)}")
        close_file()
    except Exception as e:
        logger.error(f"Error in startup method: {str(e)}")
        logger.error(traceback.format_exc())
        close_file()
    
def close_file(*args):
    logger.info("Attempting to close document")
    time.sleep(0.2)
    try:
        if myDocument:
            myDocument.close(True)
            logger.info("Document closed successfully")
        else:
            logger.warning("Document reference is None, cannot close")
    except Exception as e:
        logger.error(f"Error closing document: {str(e)}")
        logger.error(traceback.format_exc())
    
    
    
    