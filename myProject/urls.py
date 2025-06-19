from django.contrib import admin
from django.urls import path, include  # include is important
from django.urls import path
from myApp.views import music_player

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('myApp.urls')),
    path('music/', music_player, name='music_player'),
    path('', include('myApp.urls')),

]
