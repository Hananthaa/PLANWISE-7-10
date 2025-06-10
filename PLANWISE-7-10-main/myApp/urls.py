from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from .views import music_player 
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Root URL mapped to home
    path('delete_exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('test/', views.test, name='test'),
    path('tasks/', views.tasks, name='tasks'),
    path('complete/<int:id>/', views.complete_task, name='complete_task'),
    path('home3/', views.dashboard, name='dashboard'),  # This matches your dashboard view
    path('forum/', views.forum_view, name='forum'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/create/', views.create_post, name='create_post'),
    path('forum/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('forum/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('music/', music_player, name='music_player'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('calendar/', views.calendar_view, name='calendar'),  # fallback current month
    path('tracker', views.tracker, name='tracker'), #tracker start
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('habits/', views.habit_tracker, name='habit_tracker'),
    path('add_topic', views.add_topic, name='add_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'), #tracker end
    path('topic_completion/<int:topic_id>/', views.topic_complete, name='topic_complete'),
    path('topic_uncompletion/<int:topic_id>/', views.topic_uncomplete, name='topic_uncomplete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)