from .models import ForumPost, Comment, Exam, Subject, Topic, Task
from .forms import ExamForm, SubjectForm, TopicForm
from .utils import get_prev_month, get_next_month

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.db.models import Q, Count
from django.http import HttpResponse

import calendar
from calendar import HTMLCalendar
from datetime import datetime, date
import pytz

from django.shortcuts import render
import holidays
from datetime import date, datetime, timedelta
from calendar import HTMLCalendar
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, HabitRecord
from datetime import date
from django.contrib.auth.decorators import login_required

from datetime import date
from myApp.models import Task, HabitRecord

from datetime import date
from django.contrib.auth.decorators import login_required
from myApp.models import Task, HabitRecord

from collections import Counter

from collections import Counter

from django.shortcuts import render, redirect
from .models import DailyNote
from .forms import DailyNoteForm
from datetime import date

from datetime import datetime
from django.utils import timezone

from django.shortcuts import render
import random

@login_required
def habit_tracker(request):
    user = request.user
    today = date.today()
    tasks = Task.objects.filter(user=user)

    # Count how many tasks share the same title
    title_counts = Counter(task.title for task in tasks)

    # Convert to list of dicts for template
    tasks_grouped = [{'title': title, 'count': count} for title, count in title_counts.items()]

    return render(request, 'myApp/habit_tracker.html', {
        'tasks_grouped': tasks_grouped,
        'today': today,
    })


@login_required
def test(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user  # Assign logged-in user
            exam.save()
            return redirect('test')  # Redirect to same page after saving
    else:
        form = ExamForm()

    exams = Exam.objects.filter(user=request.user)

    # Generate consistent colors for each subject
    subject_colors = {}
    color_palette = [
        '#FFD700', '#1E90FF', '#FF6347', '#3CB371', '#BA55D3',
        '#FF4500', '#00CED1', '#FF69B4', '#8A2BE2', '#00FA9A'
    ]
    color_index = 0

    for exam in exams:
        if exam.subject not in subject_colors:
            subject_colors[exam.subject] = color_palette[color_index % len(color_palette)]
            color_index += 1

    return render(request, 'myApp/assign&exambox.html', {
        'form': form,
        'exams': exams,
        'subject_colors': subject_colors
    })

@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    if request.method == 'POST':
        exam.delete()
        return redirect('test')

    return HttpResponse("This view only accepts POST requests to delete an exam.")

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
    return redirect('tasks')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.date = request.POST.get('date')
        task.save()
        return redirect('tasks')

    return render(request, 'myApp/edit_task.html', {'task': task})

@login_required
def tasks(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(user=request.user) | Q(shared_with=request.user),
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()
    else:
        tasks = Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user)).distinct()

    today = date.today()
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed

    for task in tasks:
        task.time_left = (task.date - today).days if task.date else None

    users = User.objects.exclude(id=request.user.id)

    return render(request, 'myApp/tasks.html', {
        'tasks': tasks,
        'completed_count': completed,
        'pending_count': pending,
        'users': users,
    })


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'myApp/home.html')

def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')

    return render(request, "myApp/signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'myApp/login.html')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user)).distinct()
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed

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

from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from datetime import timedelta, date
from django.db.models import Count
from datetime import date, timedelta

from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task
from datetime import date, timedelta
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from .models import Task

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from .models import Task

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from .models import Task

from django.utils import timezone  # ✅ Ensure this is imported

from .models import Task  # Add this import

from .utils import TaskCalendar  # Import the custom calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return HttpResponseRedirect(reverse('chat', args=[other_user.username]))

    return render(request, 'myApp/chat.html', {
        'other_user': other_user,
        'messages': messages,
    })

@login_required
def user_list(request):
    query = request.GET.get('q')
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

    return render(request, 'myApp/user_list.html', {
        'users': users,
        'query': query,
    })

@login_required
def calendar_view(request):
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    first_day = date(year, month, 1)

    prev_month_date = first_day - timedelta(days=1)
    next_month_date = (first_day + timedelta(days=31)).replace(day=1)

    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%B %d, %Y').date()
        except ValueError:
            try:
                selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            except ValueError:
                selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    note, created = DailyNote.objects.get_or_create(user=request.user, date=selected_date)
    tasks = Task.objects.filter(user=request.user)

    # Use the custom calendar class
    cal = TaskCalendar(tasks).formatmonth(year, month)

    if request.method == 'POST':
        if 'save_note' in request.POST:
            form = DailyNoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return redirect(f"{request.path}?year={year}&month={month}&date={selected_date}")
        elif 'delete_note' in request.POST:
            note.delete()
            return redirect(f"{request.path}?year={year}&month={month}&date={selected_date}")
    else:
        form = DailyNoteForm(instance=note)

    context = {
        'calendar': mark_safe(cal),
        'month_name': calendar.month_name[month],
        'year': year,
        'prev_month': {'year': prev_month_date.year, 'month': prev_month_date.month},
        'next_month': {'year': next_month_date.year, 'month': next_month_date.month},
        'form': form,
        'selected_date': selected_date,
        'note': note,
        'tasks': tasks,
    }

    return render(request, 'myApp/calendar.html', context)


@login_required
def add_task(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        shared_user_ids = request.POST.getlist('shared_with')

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

    if request.user != task.user and request.user not in task.shared_with.all():
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('tasks')

    task.delete()
    return redirect('tasks')

@login_required
def forum_view(request):
    query = request.GET.get('q')
    if query:
        posts = ForumPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts = ForumPost.objects.all().order_by('-created_at')

    return render(request, 'myApp/forum.html', {'posts': posts, 'query': query})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')  # get comments for this post

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            return redirect('post_detail', post_id=post.id)

    return render(request, 'myApp/post_detail.html', {'post': post, 'comments': comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        ForumPost.objects.create(user=request.user, title=title, content=content, image=image)
        return redirect('forum')
    return render(request, 'myApp/create_post.html')


@login_required
def music_player(request):
    malaysia_timezone = pytz.timezone('Asia/Kuala_Lumpur')
    malaysia_time = datetime.now(malaysia_timezone).strftime('%H:%M:%S')
    return render(request, 'myApp/music_player.html', {
        'malaysia_time': malaysia_time
    })


def your_calendar_view(request):
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    my_holidays = holidays.Malaysia(years=year)

    class HolidayCalendar(HTMLCalendar):
        def formatday(self, day, weekday):
            if day == 0:
                return '<td></td>'
            current_date = date(year, month, day)
            holiday_name = my_holidays.get(current_date)
            if holiday_name:
                # Highlight holiday date
                return f'<td style="background-color:#ffcccc;" title="{holiday_name}"><strong>{day}</strong></td>'
            return f'<td>{day}</td>'

    cal = HolidayCalendar().formatmonth(year, month)

    current_date = date(year, month, 1)
    prev_month = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    context = {
        'calendar': cal,
        'month_name': current_date.strftime('%B'),
        'year': year,
        'prev_month': {'month': prev_month.month, 'year': prev_month.year},
        'next_month': {'month': next_month.month, 'year': next_month.year},
    }

    return render(request, 'myApp/your_template.html', context)

#tracker
def tracker(request):
    print ("hi++++++++++++++++++++++++++++")
    if request.method == 'POST':
        print("Wowo post :O")
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SubjectForm()
    subject = Subject.objects.all()  # Retrieve all saved exams
    return render(request, 'myapp/tracker.html',
                  {'subject': subject})

def display_exams(request):
    exams = Exam.objects.all()  # Retrieve all Exam objects from the database
    return render(request, 'display_exams.html', {'exams': exams})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        subject.delete()
        return redirect('tracker')
    return HttpResponse("This view only accepts POST requests to delete an exam.")

def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        subject_id = request.POST.get('subject_id')
        subject = get_object_or_404(Subject, pk=subject_id)
        print (subject_id + '========================')
        print (subject.subject + '--------------------------')
        if form.is_valid():
            topic = form.save(commit=False)
            print (topic.title + '0000000000000000000000000000000000')
            topic.subject = subject
            topic.save()
            return redirect('tracker')
    else:
        return redirect('tracker')


@login_required
def tasks(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(
        Q(user=request.user) | Q(shared_with=request.user),
        Q(title__icontains=query) | Q(description__icontains=query)
    ).distinct() if query else Task.objects.filter(Q(user=request.user) | Q(shared_with=request.user)).distinct()

    today = date.today()
    for task in tasks:
        task.time_left = (task.date - today).days if task.date else None

    completed = tasks.filter(completed=True).count()
    total = tasks.count()
    pending = total - completed
    users = User.objects.exclude(id=request.user.id)

    return render(request, 'myApp/tasks.html', {
        'tasks': tasks,
        'completed_count': completed,
        'pending_count': pending,
        'users': users,
    })


def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.method == 'POST':
        topic.delete()
        return redirect('tracker')

    return HttpResponse("This view only accepts POST requests to delete a topic.")

#save topic
def topic_complete(request, topic_id):
    if request.method == 'POST':
        print ("checkbox checked*********")
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.topiccomplete = True
        topic.save()
        return redirect('tracker')
    else:
        return HttpResponse("Method Not Allowed", status=405)

def topic_uncomplete(request, topic_id):
    if request.method == 'POST':
        print ("checkbox unchecked*********")
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.topiccomplete = False
        topic.save()
        return redirect('tracker')
    else:
        return HttpResponse("Method Not Allowed", status=405)



def your_calendar_view(request):
    # existing code ...
    
    motivational_quotes = [
        "Believe in yourself and all that you are.",
        "Your limitation—it’s only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn’t just find you. You have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Don’t stop when you’re tired. Stop when you’re done.",
        "Wake up with determination. Go to bed with satisfaction.",
        "Do something today that your future self will thank you for."
    ]
    
    random_quote = random.choice(motivational_quotes)

    context = {
        # your existing context variables...
        "quote": random_quote,
    }
    return render(request, 'myApp/your_template_name.html', context)