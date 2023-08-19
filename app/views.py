from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import  auth
from django.contrib import messages
from .models import Task, TaskCategory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.db.models import Q

date_string = "2023-08-18"
date_format = "%Y-%m-%d"
time_string = "14:30"
time_format = "%H:%M"

current_date = date.today()
current_time = datetime.now().time()
# Create your views here.
def index(request):
    update_tasks()
    return render(request, "app/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if not username or not email or not password or not password2:
            messages.warning(request, "Incomplete credentials provided")
            return redirect('signup')
        if password != password2:
            messages.warning(request, "Password did not  match!")
            return redirect("signup")
        if len(password) < 8:
            messages.warning(request, "Password must be minimum of 8 characters")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exist, choose another one")
            return redirect("signup")
        user = User.objects._create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account Created successfully, login to proceed")
        return redirect('login')

    return render(request, "app/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username  or not password:
            messages.warning(request, "Incomplete credentials provided")
            return redirect('login')
        user = User.objects.filter(username=username).exists()
        if not user:
            messages.warning(request, "Invalid Username")
            return redirect('login')
        user = auth.authenticate(username=username,password=password)
        if not user:
            messages.warning(request, "Invalid Password")
            return redirect('login')
        auth.login(request, user)
        messages.success(request, "Login successful")
        return redirect('dashboard')
    return render(request, "app/login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def dashboard(request):
    active = request.GET.get('active')
    if active:
        active = "active"
    completed = request.GET.get('completed')
    if completed:
        completed = "completed"
    expired = request.GET.get('expired')
    if expired:
        expired = "expired"
    print(active, completed, expired)
    user = request.user
    tasks = Task.objects.filter(owner = user)
    if active or completed or expired:
        tasks = tasks.filter(Q(status=active) | Q(status=completed) | Q(status=expired))
    active = tasks.filter(status="active")
    completed = tasks.filter(status="completed")
    expired = tasks.filter(status="expired")
    context = {"tasks": tasks, "active": len(active), "completed": len(completed), "expired":len((expired))}
    return render(request, "app/dashboard.html", context)

@login_required
def create_task(request):
    print("yes")
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        due_time = request.POST.get("due_time")
        priority = request.POST.get("priority")
        category = request.POST.get("category")
        if not title or not description or not due_date or not due_time or not priority or not category:
            messages.warning(request, "Incomplete details")
            return redirect(reverse('create'))
        due_date = datetime.strptime(due_date, date_format).date()
        if due_date < current_date:
            messages.warning(request, "Date already elapse")
            return redirect(reverse('create'))
        due_time = datetime.strptime(due_time, time_format).time()
        if current_date == due_date and current_time > due_time:
            messages.warning(request, "Time already elapse")
            return redirect(reverse('create'))
        category = get_object_or_404(TaskCategory, name=category)
        task = Task.objects.create(title=title, description = description, due_date = due_date,
        due_time = due_time, priority=priority, category=category, owner=request.user)
        task.save()
        messages.success(request, "Task created")
        return redirect('dashboard')
    categories = TaskCategory.objects.all()
    context = {"categories": categories}
    return render(request, "app/create.html", context)

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if task.owner != request.user:
        messages.warning(request, "Unauthorized")
        return redirect('dashboard')
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        due_time = request.POST.get("due_time")
        priority = request.POST.get("priority")
        category = request.POST.get("category")
        if not title or not description or not due_date or not due_time or not priority or not category:
            messages.warning(request, "Incomplete details")
            return redirect(reverse('edit', kwargs={'id': id}))
        due_date = datetime.strptime(due_date, date_format).date()
        if task.due_date > due_date:
            messages.warning(request, "Date already elapse")
            return redirect(reverse('edit', kwargs={'id': id}))
        due_time = datetime.strptime(due_time, time_format).time()
        if task.due_date == due_date and task.due_time < due_time:
            messages.warning(request, "Time already elapse")
            return redirect(reverse('edit', kwargs={'id': id}))
        category = get_object_or_404(TaskCategory, name=category)
        task.title = title
        task.description = description
        task.due_date = due_date
        task.due_time = due_time
        task.priority = priority
        task.category = category
        task.status =  "active"
        task.save()
        messages.success(request, "Task Updated")
        return redirect('dashboard')
    categories = TaskCategory.objects.all()
    context = {"task": task, "categories": categories}
    return render(request, "app/edit.html", context)

def completed(request, id):
    task = get_object_or_404(Task, id=id)
    if task.owner != request.user:
        messages.warning(request, "Unauthorized")
        return redirect('dashboard')
    task.status = "completed"
    task.save()
    messages.success(request, "marked as complete")
    return redirect('dashboard')

def update_tasks():
    result = Task.objects.filter(status="active")
    for task in result:
        if (current_date > task.due_date) or (current_date == task.due_date and current_time > task.due_time):
            task.status = "expired"
            task.save()

def delete(request, id):
    task = get_object_or_404(Task, id=id)
    if task.owner != request.user:
        messages.warning(request, "Unauthorized")
        return redirect('dashboard')
    task.delete()
    messages.info(request, "Task deleted")
    return redirect('dashboard')


def error_404_view(request, exception):
    return render(request, 'app/error.html', status=404)

def error_500_view(request):
    return render(request, 'app/error.html', status=500)