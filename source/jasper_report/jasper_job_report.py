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
from librepy.pybrex.values import JASPER_REPORTS_DIR

def job_report(start_date, end_date, search_term, logger, *args):
    logger.info("Starting JasperJobReport")

    report_path = os.path.join(JASPER_REPORTS_DIR, 'job_history_report.jrxml')
    
    # Define report parameters
    report_params = {
        'start_date': {
            'value': start_date,
            'type': 'uno_date'
        },
        'end_date': {
            'value': end_date,
            'type': 'uno_date'
        },
        'search_term': {
            'value': search_term,
            'type': 'string'
        }
    }

    main(report_path, report_params)

    logger.info("JasperJobReport completed")