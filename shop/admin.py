from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Category, Product, Profile, Order, OrderEntry
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

class OrderEntryInline(admin.TabularInline):
    model = OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]

class OrderEntryAdmin(admin.ModelAdmin):
    pass

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(OrderEntry, OrderEntryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
