from datetime import datetime


def custom_datetime():
    date_t = str(datetime.now())[:-7]
    date_t = date_t.replace(' ', '_')
    date_t = date_t.replace(':', '-')
    
    return date_t  # datetime returned as yyyy-mm-dd_hh-mm-ss


