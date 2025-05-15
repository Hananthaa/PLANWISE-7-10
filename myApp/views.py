from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'myApp/home.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    
    return render(request, "myApp/signup.html")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print("AUTH RESULT:", user)  # DEBUG LINE

        if user is not None:
            login(request, user)
            print("LOGIN SUCCESSFUL")  # DEBUG LINE
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            print("LOGIN FAILED")  # DEBUG LINE

    return render(request, 'myApp/login.html')

# Dashboard View
@login_required
def dashboard(request):
    return render(request, 'myApp/home3.html')  # Pointing to your home3.html template




