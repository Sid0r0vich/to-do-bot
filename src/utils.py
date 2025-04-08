from datetime import datetime

def get_current_day_num():
    epoch = datetime(1970, 1, 1)
    current_date = datetime.now()
    return (current_date - epoch).days