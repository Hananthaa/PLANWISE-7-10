from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('habits/', views.habits_tracker, name='habits_tracker'),

]
