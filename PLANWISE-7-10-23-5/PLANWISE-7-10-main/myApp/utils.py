from datetime import datetime, timedelta

def get_prev_month(date):
    """Returns the first day of the previous month based on the given date."""
    first = date.replace(day=1)
    prev_month = first - timedelta(days=1)
    return prev_month.replace(day=1)

def get_next_month(date):
    """Returns the first day of the next month based on the given date."""
    next_month = date.replace(day=28) + timedelta(days=4)  # move to next month
    return next_month.replace(day=1)

def get_month_range(date):
    """Returns a list of dates for the month of the given date."""
    start = date.replace(day=1)
    next_month = get_next_month(start)
    days = (next_month - start).days
    return [start + timedelta(days=i) for i in range(days)]
