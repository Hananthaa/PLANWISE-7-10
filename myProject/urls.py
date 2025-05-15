from django.contrib import admin
from django.urls import path
from myApp import views  # import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),  # This should already be defined in your views
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Add this line to map the root URL to the home view
    path('home3/', views.dashboard, name='dashboard'),
]