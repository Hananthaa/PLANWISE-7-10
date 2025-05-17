from .models import ForumPost, Comment
from .utils import get_prev_month, get_next_month
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
import calendar
from datetime import datetime, date
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.db.models import Count
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ForumPost
from django.contrib import messages

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if request.user != post.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect('forum')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'myApp/edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)

    if request.user != post.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect('forum')

    post.delete()
    return redirect('forum')

def complete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.completed = True
    task.save()
    return redirect('tasks')  # Replace with your actual view name

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.date = request.POST.get('date')
        task.save()
        return redirect('tasks')

    return render(request, 'myApp/edit_task.html', {'task': task})

@login_required
def tasks(request):
    tasks = Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user)).distinct()
    today = date.today()
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed

    for task in tasks:
        task.time_left = (task.date - today).days if task.date else None

    users = User.objects.exclude(id=request.user.id)  # For share dropdown if needed

    return render(request, 'myApp/tasks.html', {
        'tasks': tasks,
        'completed_count': completed,
        'pending_count': pending,
        'users': users,   # Pass users here if your tasks.html form needs to show the share options
    })

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Home View
def home(request):
    return render(request, 'myApp/home.html')


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

        user = authenticate(request, username=username, password=password)
        print("AUTH RESULT:", user)  # DEBUG LINE

        if user is not None:
            login(request, user)
            print("LOGIN SUCCESSFUL")  # DEBUG LINE
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            print("LOGIN FAILED")  # DEBUG LINE

    return render(request, 'myApp/login.html')


 # make sure these are defined

from django.db.models import Count  # make sure this is at the top

@login_required
def dashboard(request):
        # Get tasks either owned by user or shared with user
        tasks = Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user)).distinct()
        total = tasks.count()
        completed = tasks.filter(completed=True).count()
        pending = total - completed

        # Forum Summary (same as before)
        forum_posts = ForumPost.objects.all()
        total_posts = forum_posts.count()
        total_replies = Comment.objects.count()

        most_active_post = (
            forum_posts.annotate(reply_count=Count('comments'))
            .order_by('-reply_count')
            .first()
        )

        return render(request, 'myApp/home3.html', {
            'total_tasks': total,
            'completed_tasks': completed,
            'pending_tasks': pending,
            'total_posts': total_posts,
            'total_replies': total_replies,
            'most_active_post': most_active_post,
        })



# Calendar View
@login_required
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

    current_date = datetime(year, month, 1)
    cal = HTMLCalendar().formatmonth(year, month)

    context = {
        'calendar': mark_safe(cal),
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'prev_month': get_prev_month(current_date),
        'next_month': get_next_month(current_date),
    }
    return render(request, 'myApp/calendar.html', context)

@login_required
def add_task(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        shared_user_ids = request.POST.getlist('shared_with')  # multiple users

        task = Task.objects.create(user=request.user, title=title, description=description, date=date)

        if shared_user_ids:
            shared_users = User.objects.filter(id__in=shared_user_ids)
            task.shared_with.set(shared_users)

        return redirect('tasks')

    return render(request, 'myApp/add_task.html', {'users': users})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    users = User.objects.exclude(id=request.user.id)

    # Allow edit only if user is owner or in shared_with
    if request.user != task.user and request.user not in task.shared_with.all():
        messages.error(request, "You don't have permission to edit this task.")
        return redirect('tasks')

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.date = request.POST.get('date')
        shared_user_ids = request.POST.getlist('shared_with')

        task.save()

        if shared_user_ids:
            shared_users = User.objects.filter(id__in=shared_user_ids)
            task.shared_with.set(shared_users)
        else:
            task.shared_with.clear()

        return redirect('tasks')

    return render(request, 'myApp/edit_task.html', {
        'task': task,
        'users': users,
    })


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Allow delete only if user is owner or in shared_with
    if request.user != task.user and request.user not in task.shared_with.all():
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('tasks')

    task.delete()
    return redirect('tasks')

@login_required
def forum_view(request):
    posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'myApp/forum.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            return redirect('post_detail', post_id=post.id)
    return render(request, 'myApp/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        ForumPost.objects.create(user=request.user, title=title, content=content)
        return redirect('forum')
    return render(request, 'myApp/create_post.html')
