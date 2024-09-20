from django.contrib import admin
from .models import Product, Logo, Slider,Order,OrderItem,Contact

# Register your models here.
admin.site.register(Product)
admin.site.register(Logo)
admin.site.register(Slider)
admin.site.register(Contact)

# admin.py

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
