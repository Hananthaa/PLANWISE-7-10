# myapp/utils.py
from calendar import HTMLCalendar
from collections import defaultdict
from datetime import date, timedelta

def identify_habits(tasks, min_repeats=3, within_days=30):
    """
    Find tasks repeated min_repeats times in the past within_days.
    """
    recent_tasks = [
        task for task in tasks
        if task.date >= date.today() - timedelta(days=within_days)
    ]

    task_counter = defaultdict(int)
    for task in recent_tasks:
        task_counter[task.description] += 1  # use .description field

    habits = {
        name: count
        for name, count in task_counter.items()
        if count >= min_repeats
    }
    return habits

class SundayHTMLCalendar(HTMLCalendar):
    def __init__(self):
        super().__init__(firstweekday=6)  # 6 represents Sunday
