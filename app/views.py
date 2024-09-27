from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from app.models import Product, ContactMessage, Subscriber, History
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    user = request.user
    my_products = Product.objects.filter(owner = user).order_by("-created_at")
    market_place = Product.objects.all().exclude(owner=user).order_by("-created_at")
    context = {
        "my_products": my_products,
        "market_place": market_place
    }
    return render (request, "index.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if not name or not email or not message:
            messages.error(request, "All fields are required")
            return redirect(contact)
        new_contact = ContactMessage.objects.create(name=name, email=email, message=message)
        new_contact.save()
        messages.success(request, "Message received successfully")
    return render(request, "contact.html")

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is required")
            return redirect(reverse('home'))
        allready_subscribe = Subscriber.objects.filter(email=email).exists()
        if allready_subscribe:
            messages.error(request, "You are already a subscriber")
            return redirect(reverse('home'))
        new_sub = Subscriber.objects.create(email=email)
        new_sub.save()
        messages.success(request, "Thank you for subscribing")
        return redirect(reverse('home'))
    return redirect(reverse('home'))

@login_required
def history(request):
    user = request.user
    record = History.objects.filter(user=user)
    context = {"history": record}
    return render(request, "history.html", context)

        