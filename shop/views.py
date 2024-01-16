from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from shop.models import *

# Create your views here.
def index(request):
    context = {
        'categories': Category.objects.all()
    }
    Category.objects.prefetch_related(Product.__name__)
    return render(request, 'shop/index.html', context)

def products_list(request):
    products = Product.objects.all()

    page_object = paginate_items(request, products)

    context = {
        'products': page_object.object_list,
        'page_object': page_object
    }
    return render(request, 'shop/products.html', context)

def category_details(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category_id)

    page_object = paginate_items(request, products)

    context = {
        'category': category,
        'products': page_object.object_list,
        'page_object': page_object
    }
    return render(request, 'shop/category.html', context)


def paginate_items(request, products, per_page=10):
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return page_object


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    profile: Profile = Profile.objects.get_or_create(user=request.user)[0]

    # TODO: method get_shopping_cart
    active_order = profile.orders.filter(status=StatusOrder.INITIAL).first()
    if not active_order:
        active_order = Order.objects.create(profile=profile, status=StatusOrder.INITIAL)

    entry = OrderEntry.objects.get_or_create(order=active_order, product=product)[0]

    entry.count += 1
    entry.save()

    return redirect('shop:detail', product_id)

@login_required
def cart(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    orders = profile.orders.filter(status=StatusOrder.INITIAL)
    Order.objects.prefetch_related('order_entries')

    entries = []
    for order in orders:
        for entry in order.order_entries.all():
            entries.append(entry)

    if len(entries) == 0:
        return render(request, 'shop/cart.html', {})
    total_price = sum([(entry.product.price * entry.count) for entry in entries])
    return render(request, 'shop/cart.html', {'entries': entries, 'total_price': total_price})

@login_required
def cart_delete(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    orders = profile.orders.filter(status=StatusOrder.INITIAL)
    for order in orders:
        order.delete()

    return redirect('shop:cart')
