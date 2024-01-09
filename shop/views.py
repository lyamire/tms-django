from django.shortcuts import get_object_or_404, render

from shop.models import Category, Product


# Create your views here.
def index(request):
    context = {
        # 'products': Product.objects.all(),
        'categories': Category.objects.all()
    }
    Category.objects.prefetch_related(Product.__name__)
    return render(request, 'shop/index.html', context)

def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/detail.html', {'product': product})

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category_id)
    context = {
        'products': products,
        'category': category
    }
    return render(request, 'shop/category.html', context)
