from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)    # This 'category_slug' comes from Category Model.
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()                              # It count the product which we bring from upper line Product model and pass to the template for use.

    context = {
        'products': products,
        'product_count' : product_count
    }

# if - else ka yaha mtlb h ki agar slug pass ho toh slug value le ae category model se then us category ko render karvade otherwise
# koi slug nahi h toh simple store page me sab dikha do.

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product
    }
    return render(request, 'store/product_detail.html', context)