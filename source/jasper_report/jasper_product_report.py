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
from librepy.jasper_report.jasper_report_manager import main
from librepy.fertilizer_cmd_ctr.data.report_dao import ReportDAO
from librepy.pybrex.values import JASPER_REPORTS_DIR
import datetime

def product_report(start_date, end_date, logger, *args):
    logger.info("Starting JasperProductReport with unit conversion fix")

    report_path = os.path.join(JASPER_REPORTS_DIR, 'product_history_report.jrxml')
    
    # Convert UNO dates to Python dates for ReportDAO
    try:
        if hasattr(start_date, 'Year'):
            py_start_date = datetime.date(start_date.Year, start_date.Month, start_date.Day)
        else:
            py_start_date = start_date
            
        if hasattr(end_date, 'Year'):
            py_end_date = datetime.date(end_date.Year, end_date.Month, end_date.Day)
        else:
            py_end_date = end_date
    except Exception as e:
        error_msg = f"Error converting dates: {e}"
        logger.error(error_msg)
        MsgBox(error_msg, 16, "Date Conversion Error")
        return
    
    # Create ReportDAO instance and generate temp table
    report_dao = ReportDAO(logger)
    temp_table_name = None
    
    try:
        # Clean up any old jasper tables first
        logger.info("Cleaning up old jasper temporary tables before creating new one")
        cleaned_count = report_dao.cleanup_old_jasper_tables()
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old jasper tables")
        
        # Create temp table with converted product data
        logger.info(f"Creating temporary table for product report: {py_start_date} to {py_end_date}")
        temp_table_name = report_dao.create_temp_product_report_table(py_start_date, py_end_date)
        
        if not temp_table_name:
            error_msg = "Failed to create temporary table for product report"
            logger.error(error_msg)
            MsgBox(error_msg, 16, "Report Generation Error")
            return
        
        logger.info(f"Successfully created temporary table: {temp_table_name}")
        
        # Define report parameters with temp table info
        report_params = {
            'start_date': {
                'value': start_date,
                'type': 'uno_date'
            },
            'end_date': {
                'value': end_date,
                'type': 'uno_date'
            },
            'temp_table_name': {
                'value': temp_table_name,
                'type': 'string'
            }
        }

        # Generate the report using temp table
        logger.info(f"Generating Jasper report using temp table: {temp_table_name}")
        main(report_path, report_params)
        
        logger.info("JasperProductReport completed successfully")
        
        # Schedule cleanup after a delay to allow Jasper Reports to finish
        # Jasper Reports runs asynchronously, so we need to delay cleanup
        import threading
        def delayed_cleanup():
            import time
            time.sleep(10)  # Wait 10 seconds for Jasper to finish
            try:
                logger.info(f"Performing delayed cleanup of temporary table: {temp_table_name}")
                cleanup_success = report_dao.cleanup_temp_table(temp_table_name)
                if cleanup_success:
                    logger.info(f"Successfully cleaned up temp table: {temp_table_name}")
                else:
                    logger.warning(f"Failed to cleanup temp table: {temp_table_name}")
            except Exception as cleanup_error:
                logger.error(f"Error during delayed temp table cleanup: {cleanup_error}")
        
        # Start cleanup thread
        cleanup_thread = threading.Thread(target=delayed_cleanup, daemon=True)
        cleanup_thread.start()
        
    except Exception as e:
        error_msg = f"Error generating product report: {e}"
        logger.error(error_msg)
        MsgBox(error_msg, 16, "Report Generation Error")
        
        # Still cleanup temp table on error (immediately since report failed)
        if temp_table_name:
            try:
                logger.info(f"Cleaning up temporary table after error: {temp_table_name}")
                cleanup_success = report_dao.cleanup_temp_table(temp_table_name)
                if cleanup_success:
                    logger.info(f"Successfully cleaned up temp table after error: {temp_table_name}")
                else:
                    logger.warning(f"Failed to cleanup temp table after error: {temp_table_name}")
            except Exception as cleanup_error:
                logger.error(f"Error during temp table cleanup after error: {cleanup_error}")