import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


def get_request_data(request):
    """Helper to extract data from POST requests (Form or JSON)"""
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return {}
    return request.POST


@csrf_exempt
def signup_view(request):
    message = ""

    if request.method == 'POST':
        data = get_request_data(request)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            message = "Username and password are required."
            if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
                return JsonResponse({"status": "error", "message": message}, status=400)
            return render(request, 'signup.html', {'message': message})

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            message = "User already exists. Please login."
            if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
                return JsonResponse({"status": "error", "message": message}, status=400)
        else:
            # Set default role specifically to prevent models validation errors
            User.objects.create_user(username=username, password=password, role='student')
            if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
                return JsonResponse({"status": "success", "message": "User created successfully"})
            return redirect('login')

    return render(request, 'signup.html', {'message': message})


@csrf_exempt
def login_view(request):
    message = ""

    if request.method == 'POST':
        data = get_request_data(request)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
                return JsonResponse({
                    "status": "success", 
                    "message": "Logged in successfully",
                    "user": {
                        "username": user.username,
                        "role": user.role
                    }
                })
            return redirect('home')
        else:
            message = "User not registered or wrong password"
            if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
                return JsonResponse({"status": "error", "message": message}, status=401)

    return render(request, 'login.html', {'message': message})


def home(request):
    if not request.user.is_authenticated:
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)
        return redirect('login')

    return render(request, 'home.html')


@csrf_exempt
def logout_view(request):
    logout(request)
    if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
        return JsonResponse({"status": "success", "message": "Logged out successfully"})
    return redirect('login')