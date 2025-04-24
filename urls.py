from django.urls import path
from calendar_app import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('tasks/', views.task_list, name='task_list'),
]