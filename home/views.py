from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Q
from .models import Product,Logo,Slider,Order,OrderItem
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
  product = Product.objects.all()
  logo = Logo.objects.all()
  slider = Slider.objects.all()
  return render(request,"home.html",
    {
    'slider':slider,
    'product':product,
    'logo':logo,
})
def product(request, post_id):
    product = get_object_or_404(Product, id=post_id)
    return render(request, 'product.html', {'product': product})


def cart(request):
    # Retrieve cart from session
    cart = request.session.get('cart', {})
    
    # Fetch products from the database
    product_ids = cart.keys()  # Get all product IDs from the cart
    products = {product.id: product for product in Product.objects.filter(id__in=product_ids)}
    
    # Prepare a list of products with quantities for the template
    cart_items = [(products.get(int(product_id)), quantity) for product_id, quantity in cart.items()]
    
    # Calculate total price
    total_price = sum(product.price * quantity for product, quantity in cart_items if product)
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('/')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Convert product_id to string to match session key
    product_id_str = str(product_id)

    # Debugging: Print current cart
    print("Initial cart contents:", cart)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
        
        request.session['cart'] = cart

        # Debugging: Print updated cart
        print("Updated cart contents:", cart)
    else:
        print("Product not found in cart:", product_id)

    return redirect('cart')

def cod(request):
    # Retrieve cart from session
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart')  # Redirect to the cart if the cart is empty
    
    # Fetch products from the database
    products = {product_id: Product.objects.get(id=int(product_id)) for product_id in cart.keys()}
    
    # Prepare a list of products with quantities for the template
    cart_items = [(products.get(product_id), quantity) for product_id, quantity in cart.items()]
    
    # Calculate total price
    total_price = sum(product.price * quantity for product, quantity in cart_items if product)
    
    return render(request, 'cod.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
def confirm_order(request):
    # Retrieve cart from session
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart')  # Redirect to the cart if the cart is empty

    # Process order here (e.g., save to database, send confirmation email)
    
    # Clear the cart
    request.session['cart'] = {}
    
    return render(request, 'order_confirmed.html')  # You might want to create this template

@require_POST
def confirm_order(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart')  # Redirect to the cart if the cart is empty

    # Retrieve form data
    full_name = request.POST.get('full_name')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')

    # Create an Order entry
    order = Order.objects.create(
        full_name=full_name,
        phone_number=phone_number,
        address=address
    )

    # Create OrderItems for each product in the cart
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
    
    # Clear the cart
    request.session['cart'] = {}

    return render(request, 'order_confirmed.html')

def search_view(request):
    query = request.GET.get('q')  # Get the search query from the request
    results = []

    if query:
        # Search for products where title or description contains the query
        results = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})