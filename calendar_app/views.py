from datetime import datetime, date
from .models import Task
from .utils import SundayHTMLCalendar
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .utils import identify_habits

def upload_background(request):
    if request.method == 'POST' and request.FILES.get('background_image'):
        image = request.FILES['background_image']
        fs = FileSystemStorage()
        filename = fs.save(f'backgrounds/{image.name}', image)
        file_url = fs.url(filename)
        request.session['background_url'] = file_url
        return redirect('home')  # Or your actual homepage/view

    return render(request, 'calendar_app/upload_background.html')



def home(request):
    return render(request, 'calendar_app/home.html')

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
    habits = identify_habits(Task.objects.all())

    for task in tasks:
        print("task  = " + str(tasks))

    # Previous / Next month logic
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        'html_calendar': html_calendar,
        'tasks': tasks,
        'month': month,
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'calendar_view': calendar_view,
        'habits' : habits,
    }
    return render(request, 'calendar_app/calendar.html', context)


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('calendar')

