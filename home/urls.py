from django.urls import path
from .views import CustomLoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('orders/', views.user_orders, name='user_orders'),
    path('product/<int:post_id>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cod/', views.cod, name='cod'),  # Add this line
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('search/', views.search_view, name='search'),
    path('login/', CustomLoginView.as_view(), name='login')
]
