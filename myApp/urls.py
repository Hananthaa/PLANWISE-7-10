from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # Root URL mapped to home
    path('home3/', views.dashboard, name='dashboard'),  # This matches your dashboard view
]
