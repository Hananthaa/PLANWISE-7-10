from .models import ForumPost, Comment, Exam, Subject, Topic, Task, Pet
from .forms import ExamForm, SubjectForm, TopicForm, ChangePet
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

from myApp.models import Pet


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

@login_required
def calendar_view(request):
    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))

    current_date = datetime(year, month, 1)

    # Get tasks for the current user, year, and month
    tasks = Task.objects.filter(user=request.user, date__year=year, date__month=month)

    # Create a dictionary mapping day -> list of task titles
    tasks_per_day = {}
    for task in tasks:
        day = task.date.day
        if day not in tasks_per_day:
            tasks_per_day[day] = []
        tasks_per_day[day].append(task.title)

    # Custom calendar class that shows task titles inside each day cell
    class TaskCalendar(HTMLCalendar):
        def formatday(self, day, weekday):
            if day == 0:
                return '<td></td>'
            # Get task titles for this day, or empty list
            task_titles = tasks_per_day.get(day, [])
            # Build HTML for the task titles (limit or scroll if too many)
            tasks_html = ''
            for title in task_titles:
                tasks_html += f'<div style="font-size: 0.75em; margin-top: 2px;">• {title}</div>'

            return f'<td><strong>{day}</strong>{tasks_html}</td>'

    cal = TaskCalendar().formatmonth(year, month)

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

def timer(request):
    if request.method == 'POST':
        print ("checkbox unchecked*********")
        topic = get_object_or_404(Topic, pk=topic_id)
        topic.topiccomplete = False
        topic.save()
        return redirect('tracker')
    else:
        return HttpResponse("Method Not Allowed", status=405)

def timer(request):
    print ("hi++++++++++++++++++++++++++++")
    return render(request, 'myApp/timerpet.html')

#Change pet
def changepet(request):
    if request.method == 'POST':
        print("Wowo post for pet :OOOOOOOOOOOOOOOOOOOOOO")
        user_id_post = request.POST.get('user') #find user id
        pet_post = request.POST.get('pet') #post pet change user choose
        pet_check = Pet.objects.filter(user_id=user_id_post).first() #current user pet 
        form = ChangePet(request.POST)

        if form.is_valid():
            
            if pet_check: #see if user have pet record 
                print(user_id_post + "QQQQQQQQQQQQQQQQQQqqq")
                pet = Pet.objects.get(user_id=user_id_post) #get record for the user (ex. user 9)
                pet.pet = pet_post
                pet.save(update_fields=['pet'])
            else: 
                print("pet form saved!!!!!!!!!!!!!1")
                form.save()
        else:
            print("not valid888888888888888888888888")
            print(form.errors)
    return redirect("/timerpet")

def getpet(request, user_id):
    if request.method == 'GET':
        print("Wowo get pet :kkkkkkkkkkkkkkkkkkkkk")
        pet = Pet.objects.get(user_id=user_id)
        return HttpResponse(pet.pet)


#Qury table get id