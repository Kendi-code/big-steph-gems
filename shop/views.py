from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from django.http import HttpResponse
from django.core.management import call_command

# TEMPORARY BACKDOOR MIGRATION VIEW
def run_jewelry_migration(request):
    """
    Temporary view to programmatically run migrations 
    on the brand new Big Steph Gems database.
    """
    try:
        call_command('migrate', interactive=False)
        return HttpResponse("<h1>Success! Big Steph Gems database tables built perfectly.</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Migration Failed</h1><p>{str(e)}</p>")

def home_view(request):
    """Renders the absolute single-page interface encompassing home, about, shop grid and contact."""
    try:
        products = Product.objects.all().order_by('-created_at')
        # Force evaluation to see if the table exists yet
        list(products[:1]) 
    except Exception:
        # Safe fallback text if the database hasn't been migrated yet
        return HttpResponse("<h1>Big Steph Gems Setup Mode</h1><p>Please type <strong>/build-new-db/</strong> at the end of your browser link to set up your tables.</p>")
        
    context = {
        'products': products,
        'brand_name': "BIG STEPH GEMS",
        'tagline': "Curated jewelry and fashion accessories for everyday style. Send us a dm and let Steph style you."
    }
    return render(request, 'shop/index.html', context)

def product_detail(request, pk):
    """Dynamic redirection target displaying fine-tuned jewelry details and explicit dealer connection points."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/detail.html', {'product': product})

@login_required
def admin_dashboard(request):
    """Custom dashboard supporting simple workflows for uploading and modifying inventory."""
    try:
        products = Product.objects.all().order_by('-created_at')
    except Exception:
        return HttpResponse("Dashboard locked until migrations are applied.")
        
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        qty = request.POST.get('quantity_in_stock')
        details = request.POST.get('details')
        dealer_handle = request.POST.get('dealer_handle')
        image = request.FILES.get('image')

        if product_id:  # Edit/Update action
            product = get_object_or_404(Product, pk=product_id)
            product.name = name
            product.price = price
            product.quantity_in_stock = qty
            product.details = details
            product.dealer_handle = dealer_handle
            if image:
                product.image = image
            product.save()
        else:  # Create action
            Product.objects.create(
                name=name, price=price, quantity_in_stock=qty, 
                details=details, dealer_handle=dealer_handle, image=image
            )
        return redirect('admin_dashboard')

    return render(request, 'shop/dashboard.html', {'products': products})

def about_view(request):
    return render(request, 'shop/about.html')

def contact_view(request):
    return render(request, 'shop/contact.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "shop/login.html")