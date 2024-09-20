from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import Profile
from django.http import HttpResponse
from django.db.models import Q
from .models import Product, Logo, Slider, Order, OrderItem
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView

# Home view
def home(request):
    product = Product.objects.all()
    logo = Logo.objects.all()
    slider = Slider.objects.all()
    return render(request, "home.html", {
        'slider': slider,
        'product': product,
        'logo': logo,
    })

# Product detail view
def product(request, post_id):
    product = get_object_or_404(Product, id=post_id)
    return render(request, 'product.html', {'product': product})



# Cart view - user specific
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}
    cart_items = [(products.get(int(product_id)), quantity) for product_id, quantity in cart.items()]
    total_price = sum(product.price * quantity for product, quantity in cart_items if product)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('/')

# Remove product from cart
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart')

# Cash on delivery view
@login_required
def cod(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')  # Redirect to the cart if empty
    
    products = {product_id: Product.objects.get(id=int(product_id)) for product_id in cart.keys()}
    cart_items = [(products.get(product_id), quantity) for product_id, quantity in cart.items()]
    total_price = sum(product.price * quantity for product, quantity in cart_items if product)
    
    return render(request, 'cod.html', {'cart_items': cart_items, 'total_price': total_price})

# Confirm order - user-specific
@require_POST
@login_required
def confirm_order(request):
    # Retrieve cart from session
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')  # Redirect to the cart if empty

    # Retrieve form data
    full_name = request.POST.get('full_name')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')

    # Create an Order entry linked to the logged-in user
    order = Order.objects.create(
        user=request.user,  # Link order to the logged-in user
        full_name=full_name,
        phone_number=phone_number,
        address=address,
    )

    # Loop through cart and create OrderItem entries for each product
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        # Create OrderItem linked to the order and product
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )

    # Clear the cart after confirming the order
    request.session['cart'] = {}

    # Return an order confirmation page or redirect to user orders page
    return render(request, 'order_confirmed.html', {'order': order})

# Search view
def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'query': query, 'results': results})

# Register user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create Profile with additional fields
            Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )

            # Log the user in after registration
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# User orders view - show only logged-in user's orders
@login_required
def user_orders(request):
    # Fetch orders related to the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Pass the orders to the template
    return render(request, 'user_orders.html', {'orders': orders})

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify the template for the login page
