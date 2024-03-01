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

    active_order = Profile.init_shopping_cart(request.user)

    entry = OrderEntry.objects.get_or_create(order=active_order, product=product)[0]

    entry.count += 1
    entry.save()

    return redirect('shop:detail', product_id)


# def init_shopping_cart(user):
#     profile: Profile = Profile.objects.get_or_create(user=user)[0]
#     if not profile.shopping_cart:
#         profile.shopping_cart = (profile.orders.filter(status=StatusOrder.INITIAL).first()
#                                  or Order.objects.create(profile=profile, status=StatusOrder.INITIAL))
#         profile.save()
#
#     return profile.shopping_cart


@login_required
def cart(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    if (not profile.shopping_cart) or len(profile.shopping_cart.order_entries.all()) == 0:
        return render(request, 'shop/cart.html', {})

    entries = profile.shopping_cart.order_entries.all().order_by('-id')

    total_price = sum([(entry.product.price * entry.count) for entry in entries])
    return render(request, 'shop/cart.html', {'entries': entries, 'total_price': total_price})

@login_required
def cart_delete(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    if profile.shopping_cart:
        profile.shopping_cart.delete()

    return redirect('shop:cart')

@login_required()
def remove_product_from_cart(request, product_id):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    entry = profile.shopping_cart.order_entries.filter(product_id=product_id).first()
    if entry:
        entry.delete()

    return redirect('shop:cart')

@login_required()
def update_product_from_cart(request, product_id):
    count = int(request.POST.get('count'))
    profile: Profile = Profile.objects.filter(user=request.user).first()

    entry = profile.shopping_cart.order_entries.filter(product_id=product_id).first()
    if entry:
        entry.count = count
        entry.save()

    return redirect('shop:cart')


@login_required()
def cart_submit(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    order = profile.shopping_cart
    order.status = StatusOrder.COMPLETED
    order.save()

    profile.shopping_cart = None
    profile.save()

    return render(request, 'shop/cart_submit.html')


@login_required()
def profile_details(request):
    if request.method == 'GET':
        profile: Profile = Profile.objects.filter(user=request.user).first()
        orders = profile.orders.exclude(status=StatusOrder.INITIAL).order_by('-id')[:5]

        context = {
            'profile': profile,
            'orders': orders,
        }

        return render(request, 'shop/profile.html', context)
    if request.method == 'POST':
        profile: Profile = Profile.objects.filter(user=request.user).first()
        first_name: str = request.POST.get('first_name')
        last_name: str = request.POST.get('last_name')
        email: str = request.POST.get('email')

        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.email = email
        profile.user.save()

        return redirect('shop:profile')

@login_required()
def profile_history_of_orders(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    orders = profile.orders.exclude(status=StatusOrder.INITIAL).order_by('-id')

    page_object = paginate_items(request, orders, 5)

    context = {
        'profile': profile,
        'orders': page_object.object_list,
        'page_object': page_object
    }

    return render(request, 'shop/history_of_orders.html', context)

@login_required()
def order_details(request, order_id: int):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    order: Order = Order.objects.filter(id=order_id).first()
    entries = []
    for entry in order.order_entries.all().order_by('id'):
        entries.append(entry)
    context = {
        'order': order,
        'profile': profile,
        'entries': entries,
    }
    return render(request, 'shop/order_detail.html', context)

@login_required()
def reorder(request, order_id):
    order_old: Order = Order.objects.filter(id=order_id).first()
    old_entries = []
    for entry in order_old.order_entries.all().order_by('id'):
        old_entries.append(entry)

    active_order = Profile.init_shopping_cart(request.user)

    for old_entry in old_entries:
        entry = OrderEntry.objects.get_or_create(order=active_order, product=old_entry.product)[0]

        entry.count = old_entry.count
        entry.save()

    return redirect('shop:cart')
