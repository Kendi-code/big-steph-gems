from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product

# ... rest of your view logic remains exactly the same ...

def home_view(request):
    """Renders the absolute single-page interface encompassing home, about, shop grid and contact."""
    products = Product.objects.all().order_by('-created_at')
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
    products = Product.objects.all().order_by('-created_at')
    
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