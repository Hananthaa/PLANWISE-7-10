from django.contrib import admin
from django.urls import path, include  # include is important

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myApp.urls')),  # include your app's urls
]
