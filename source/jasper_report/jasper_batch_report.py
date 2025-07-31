import os
from librepy.jasper_report.jasper_report_manager import main
from librepy.pybrex.values import JASPER_REPORTS_DIR

def batch_report(job_id, logger, sort_info=None, *args):
    logger.info("Starting JasperBatchReport")

    report_path = os.path.join(JASPER_REPORTS_DIR, 'batch_report.jrxml')
    
    # Build report parameters
    report_params = {
        'job_id': {
            'value': job_id,
            'type': 'integer'
        }
    }
    
    # Add sort parameters if provided
    if sort_info:
        logger.info(f"Using custom sort: {sort_info['column']} {sort_info['direction']}")
        report_params['sort_column'] = {
            'value': sort_info['column'],
            'type': 'string'
        }
        report_params['sort_direction'] = {
            'value': sort_info['direction'],
            'type': 'string'
        }
    else:
        logger.info("Using default sort: product_name ASC")
        # Provide default values for when no sort is specified
        report_params['sort_column'] = {
            'value': 'product_name',
            'type': 'string'
        }
        report_params['sort_direction'] = {
            'value': 'ASC',
            'type': 'string'
        }

    main(report_path, report_params)

    logger.info("JasperBatchReport completed")
