from django.contrib import admin
from .models import Product, Logo, Slider,Order,OrderItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Logo)
admin.site.register(Slider)
admin.site.register(OrderItem)
admin.site.register(Order)