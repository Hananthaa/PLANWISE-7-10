from django.urls import path
from calendar_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('upload-background/', views.upload_background, name='upload_background'),
    path('home/', views.home, name='home'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
