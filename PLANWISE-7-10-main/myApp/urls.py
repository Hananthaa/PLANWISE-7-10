from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
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
    path('tracker', views.tracker, name='tracker'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('add_topic/', views.add_topic, name='add_topic'),
]
