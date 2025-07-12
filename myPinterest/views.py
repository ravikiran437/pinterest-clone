from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myPinterest.models import Pin

def signin_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Account not found!")
            return redirect('signin')

        user = authenticate(username=email, password=password)
        if not user:
            messages.error(request, "Incorrect password!")
            return redirect("signin")

        login(request, user)
        messages.success(request, "Login successfully")
        return redirect("home")

    return render(request, 'project/index.html')


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        user = User.objects.create_user(
            username=email, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('signin')

    return render(request, 'project/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logout !")
    return redirect('signin')


@login_required(login_url='signin')
def home_view(request):
    pins = Pin.objects.order_by('?')
    return render(request, 'project/home.html', {'pins': pins})


@login_required(login_url='signin')
def specific_view(request,pin_id):
    pin = Pin.objects.get(id=pin_id)
    related_pins = Pin.objects.filter(category=pin.category).exclude(id=pin.id).order_by("?")
   
    return render(request, 'project/single.html', {
        'pin': pin,
        'related_pins': related_pins
    })

def user_view(request):
    return render(request,'project/user_details.html')