'''
Utility module for converting between Python types and UNO types.

This module provides functions to convert Python standard types (datetime, date, etc.)
to their UNO equivalents for use with LibreOffice UNO API.
'''

import uno
import datetime

def python_date_to_uno(py_date):
    """
    Convert Python datetime.date to com.sun.star.util.Date.
    
    Args:
        py_date (datetime.date): Python date object to convert
        
    Returns:
        com.sun.star.util.Date or None: Converted UNO date object, or None if input is None
    """
    if not py_date:
        return None
        
    try:
        uno_date = uno.createUnoStruct("com.sun.star.util.Date")
        uno_date.Year = py_date.year
        uno_date.Month = py_date.month
        uno_date.Day = py_date.day
        return uno_date
    except Exception as e:
        print(f"Error converting date {py_date} to UNO struct: {str(e)}")
        return None

def python_datetime_to_uno(py_datetime):
    """
    Convert Python datetime.datetime to com.sun.star.util.DateTime.
    
    Args:
        py_datetime (datetime.datetime): Python datetime object to convert
        
    Returns:
        com.sun.star.util.DateTime or None: Converted UNO datetime object, or None if input is None
    """
    if not py_datetime:
        return None
        
    try:
        uno_datetime = uno.createUnoStruct("com.sun.star.util.DateTime")
        uno_datetime.Year = py_datetime.year
        uno_datetime.Month = py_datetime.month
        uno_datetime.Day = py_datetime.day
        uno_datetime.Hours = py_datetime.hour
        uno_datetime.Minutes = py_datetime.minute
        uno_datetime.Seconds = py_datetime.second
        uno_datetime.NanoSeconds = py_datetime.microsecond * 1000
        return uno_datetime
    except Exception as e:
        print(f"Error converting datetime {py_datetime} to UNO struct: {str(e)}")
        return None

def python_time_to_uno(py_time):
    """
    Convert Python datetime.time to com.sun.star.util.Time.
    
    Args:
        py_time (datetime.time): Python time object to convert
        
    Returns:
        com.sun.star.util.Time or None: Converted UNO time object, or None if input is None
    """
    if not py_time:
        return None
        
    try:
        uno_time = uno.createUnoStruct("com.sun.star.util.Time")
        uno_time.Hours = py_time.hour
        uno_time.Minutes = py_time.minute
        uno_time.Seconds = py_time.second
        uno_time.NanoSeconds = py_time.microsecond * 1000 if hasattr(py_time, 'microsecond') else 0
        return uno_time
    except Exception as e:
        print(f"Error converting time {py_time} to UNO struct: {str(e)}")
        return None

def auto_convert_to_uno(value):
    """
    Automatically convert Python values to UNO equivalents based on type.
    
    This is a convenience function that detects the type of the input value
    and calls the appropriate converter function.
    
    Args:
        value: Python value to convert
        
    Returns:
        Converted UNO object or original value if no conversion needed
    """
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return python_date_to_uno(value)
    elif isinstance(value, datetime.datetime):
        return python_datetime_to_uno(value)
    elif isinstance(value, datetime.time):
        return python_time_to_uno(value)
    else:
        # Return original value for types that don't need conversion
        return value