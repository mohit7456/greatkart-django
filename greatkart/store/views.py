from django.shortcuts import render, get_object_or_404, HttpResponse
from . models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)    # This 'category_slug' comes from Category Model.
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()                              # It count the product which we bring from upper line Product model and pass to the template for use.

    context = {
        'products': paged_products,
        'product_count' : product_count,
    }

# if - else ka yaha mtlb h ki agar slug pass ho toh slug value le ae category model se then us category ko render karvade otherwise
# koi slug nahi h toh simple store page me sab dikha do.

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if "keyword" in request.GET:                                     # We checking GET request conatining 'keyword'?
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))   # filter(Q(description__icontains=keyword) | Q(product_name__iconatins=keyword)) -->It simply search the things in description and product_name where it available.
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)