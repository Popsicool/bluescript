from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import auth, User

# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if not username or not email or not first_name or not last_name or not password or  not cpassword:
            messages.error(request, "All fields are required")
            return redirect(signup)
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            messages.error(request, "Username already taken")
            return redirect(signup)
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            messages.error(request, "Username already taken")
            return redirect(signup)
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect(signup)
        if password != cpassword:
            messages.error(request, "Password does not match")
            return redirect(signup)
        new_user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        new_user.set_password(password)
        new_user.save()
        messages.success(request, "Account created successfully")
        return redirect(login)
    return render(request, "signup.html")


def login(request):
    next = request.GET.get("next")
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect(login)
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Invalid credentials")
            return redirect(login)
        auth.login(request, user)
        return redirect( next or reverse("home"))

    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect(login)