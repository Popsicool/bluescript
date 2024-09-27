from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from app.models import Product, Review, History
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create_product(request):
    user = request.user
    if  request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        if not name or not quantity or not price or not image:
            messages.error(request, "All fields required")
            return redirect(create_product)
        new_product = Product.objects.create(
            name=name,
            quantity= quantity,
            image=image,
            price = price,
            decription = description,
            owner = user
        )
        new_product.save()
        messages.success(request, "Product Added successfully")
        return redirect(reverse("home"))
        
    return render(request, "create_product.html")


@login_required
def shop_product(request, id):
    user = request.user
    prod = Product.objects.filter(id=id).first()
    if not prod:
        messages.error(request, "Product Not found")
        return redirect(reverse("home"))
    if user == prod.owner:
        messages.error(request, "You can't buy your own product")
        return redirect(reverse("home"))
    
    all_review = Review.objects.filter(product=prod).order_by("-created_at")
    context = {"product": prod, "reviews": all_review}


    if request.method == "POST":
        quantity  = request.POST.get("qty")
        quantity = int(quantity)
        if prod.quantity < quantity:
            messages.error(request, "Not enough  quantity")
            return redirect(reverse("home"))
        prod.quantity -= quantity
        History.objects.create(
            user=user,
            product=prod,
            amount = quantity * prod.price,
            quantity=quantity
        )
        if prod.quantity == 0:
            prod.is_available = False
        prod.save()
        messages.success(request, "Order places successfully")
        return redirect(reverse("home"))
    return render(request, "shop.html", context)



@login_required
def edit_product(request, id):
    user = request.user
    prod = Product.objects.filter(id=id).first()
    if not prod:
        messages.error(request, "Product Not found")
        return redirect(reverse("home"))
    if user != prod.owner:
        messages.error(request, "Unauthorized")
        return redirect(reverse("home"))
    context = {"product": prod}
    if  request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        if not name or not quantity or not price:
            messages.error(request, "All fields required")
            return redirect(edit_product)
        prod.name = name
        prod.quantity = quantity
        prod.price = price
        prod.decription = description
        if image:
            prod.image =  image
        prod.save()
        messages.success(request, "Product Added successfully")
        return redirect(reverse("home"))
        
    return render(request, "edit_product.html", context)


@login_required
def delete_product(request, id):
    user = request.user
    prod = Product.objects.filter(id=id).first()
    if not prod:
        messages.error(request, "Product Not found")
        return redirect(reverse("home"))
    if user != prod.owner:
        messages.error(request, "Unauthorized")
        return redirect(reverse("home"))
    prod.delete()
    messages.success(request, "Product successfully deleted")
    return redirect(reverse("home"))
