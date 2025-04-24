# myapp/views.py
from django.shortcuts import render, redirect
from datetime import datetime, date
from collections import defaultdict
from .models import Task
from .utils import SundayHTMLCalendar

def calendar_view(request, year=None, month=None):
    today = date.today()
    if not year or not month:
        year = today.year
        month = today.month
    else:
        year = int(year)
        month = int(month)

    if request.method == 'POST':
        task_date = request.POST.get('date')
        task_desc = request.POST.get('description')
        if task_date and task_desc:
            task_date = datetime.strptime(task_date, '%Y-%m-%d').date()
            Task.objects.create(date=task_date, description=task_desc)
            return redirect('calendar', year=task_date.year, month=task_date.month)

    # Initialize the custom calendar
    cal = SundayHTMLCalendar()
    html_calendar = cal.formatmonth(year, month)

    # Group tasks by date
    tasks = Task.objects.filter(date__month=month, date__year=year)
    task_dict = defaultdict(list)
    for task in tasks:
        task_dict[task.date].append(task.description)

    # Previous / Next month logic
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        'html_calendar': html_calendar,
        'tasks': task_dict,
        'month': month,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'calendar_app/calendar.html', context)

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})