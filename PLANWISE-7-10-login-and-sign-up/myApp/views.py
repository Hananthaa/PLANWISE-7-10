from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import calendar
from datetime import datetime, date
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.db.models import Count
from datetime import datetime

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.date = request.POST.get('date')
        task.save()
        return redirect('home')

    return render(request, 'myApp/edit_task.html', {'task': task})

@login_required
def home(request):
    tasks = Task.objects.all()
    today = date.today()

    for task in tasks:
        if task.date:
            task.time_left = (task.date - today).days
        else:
            task.time_left = None  # fallback if date is missing

    return render(request, 'myApp/home.html', {'tasks': tasks})

@login_required
def habits_tracker(request):
    # Group tasks by their title and count occurrences
    tasks_count = Task.objects.filter(user=request.user) \
        .values('title') \
        .annotate(task_count=Count('title')) \
        .order_by('title')  # Optionally, order by task name

    return render(request, 'habits_tracker.html', {'tasks_count': tasks_count})

def calendar_view(request):
    year = request.GET.get('year')
    month = request.GET.get('month')

    if year and month:
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            year, month = datetime.today().year, datetime.today().month
    else:
        year, month = datetime.today().year, datetime.today().month

    cal = HTMLCalendar().formatmonth(year, month)
    context = {
        'calendar': mark_safe(cal),
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_month': get_prev_month(year, month),
        'next_month': get_next_month(year, month),
    }
    return render(request, 'calendar.html', context)


def get_prev_month(year, month):
    if month == 1:
        return {'month': 12, 'year': year - 1}
    else:
        return {'month': month - 1, 'year': year}


def get_next_month(year, month):
    if month == 12:
        return {'month': 1, 'year': year + 1}
    else:
        return {'month': month + 1, 'year': year}


@login_required
@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')  # ✅ capture description
        date = request.POST.get('date')

        # ✅ Create a new task with description included
        Task.objects.create(user=request.user, title=title, description=description, date=date)

        return redirect('home')

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'myApp/home.html', {'tasks': tasks})


@login_required
def delete_task(request, task_id):
    Task.objects.filter(id=task_id, user=request.user).delete()
    return redirect('home')


def logout_view(request):
    logout(request)
    return redirect('login')


# Signup View
def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')

    return render(request, "myApp/signup.html")


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')  # redirect to home page or another page
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "myApp/login.html")
