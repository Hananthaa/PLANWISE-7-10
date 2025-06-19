from datetime import datetime, timedelta
from datetime import date

import calendar
from django.utils.html import format_html
from .models import Task

class TaskCalendar(calendar.HTMLCalendar):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks

    def formatday(self, day, weekday, year, month):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        current_date = date(year, month, day)
        day_tasks = self.tasks.filter(date=current_date)

        task_html = ''
        for task in day_tasks:
            status = "✅" if task.completed else "❌"
            task_html += f'{status} {task.title}'

        return format_html(
            '<td><strong>{}</strong><br>{}</td>',
            day,
            task_html or ''
        )

    def formatweek(self, theweek, year, month):
        week_html = ''.join(self.formatday(d, wd, year, month) for (d, wd) in theweek)
        return f'<tr>{week_html}</tr>'

    def formatmonth(self, year, month, withyear=True):
        weeks = self.monthdays2calendar(year, month)
        html = f'<table border="0" cellpadding="0" cellspacing="0" class="month">\n'
        html += f'{self.formatmonthname(year, month, withyear=withyear)}\n'
        html += f'{self.formatweekheader()}\n'
        for week in weeks:
            html += f'{self.formatweek(week, year, month)}\n'
        html += '</table>'
        return html

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
