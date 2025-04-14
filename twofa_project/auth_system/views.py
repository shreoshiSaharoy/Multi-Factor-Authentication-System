from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, logout
from rest_framework.decorators import api_view
import pyotp
from django.core.mail import send_mail
from .utils import send_sms_otp  

User = get_user_model()

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    phone = request.data.get("phone")
    password = request.data.get("password")
    preferred_method = request.data.get("preferred_otp_method", "email")  # default to email

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User(username=username)
    user.email = email
    user.phone = phone
    user.preferred_otp_method = preferred_method  # Save preference
    user.set_password(password)
    user.set_otp_secret()
    user.save()

    return JsonResponse({"message": "User registered successfully"})

@api_view(['POST'])
def login_request(request):
    username = request.data.get("username")
    password = request.data.get("password")
    via = request.data.get("via", "email")  # Default to email if not provided

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    totp = pyotp.TOTP(user.get_otp_secret())
    otp = totp.now()

    if via == 'sms':
        phone_number = user.phone
        send_sms_otp(phone_number, otp)
        message = "OTP sent via SMS"
    else:
        send_mail(
            "Your Login OTP",
            f"Your OTP for login is: {otp}",
            "no-reply@yourdomain.com",
            [user.email],
            fail_silently=False,
        )
        message = "OTP sent via Email"

    return JsonResponse({"message": message})

@api_view(['POST'])
def login_verify(request):
    username = request.data.get("username")
    otp = request.data.get("otp")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=400)

    totp = pyotp.TOTP(user.get_otp_secret())
    if totp.verify(otp, valid_window=1):
        return JsonResponse({"message": "Login successful", "redirect": "/dashboard/"})
    else:
        return JsonResponse({"error": "Invalid OTP"}, status=400)

def home(request):
    #return HttpResponse("<h1>Welcome to the 2FA System</h1><p>Use /auth/register/ and /auth/login/ to test authentication.</p>")
    return render(request, "home.html")

def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("/")