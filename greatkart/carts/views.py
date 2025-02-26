from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

# This function take sesssion id from cart if it is not there then it create it.
def _cart_id(request):                       # if we use Underscore(_) before function name then it consider as Private Function.
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) # Get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []  
        if request.method == 'POST':                 # Taking value From POST URL
            for item in request.POST:                # it received colour
                key = item                           # if color is black
                value = request.POST[key]            # black will store in value


                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)  # __iexact means it ignore captal or small letters and here we check that the color or size come from url present in our db or not.
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)              
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)


            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                # create a new cart item
                if len(product_variation) > 0:                                                           
                    item.variations.clear()
                    item.variations.add(*product_variation)                                                                                                                                                
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0: 
                cart_item.variations.clear()                                                         
                cart_item.variations.add(*product_variation)  
            cart_item.save()
        
        return redirect('cart')
    
    # If user is not authenticated.
    else:
        product_variation = []  
        if request.method == 'POST':                 # Taking value From POST URL
            for item in request.POST:                # it received colour
                key = item                           # if color is black
                value = request.POST[key]            # black will store in value


                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)  # __iexact means it ignore captal or small letters and here we check that the color or size come from url present in our db or not.
                    product_variation.append(variation)
                except:
                    pass
        

        # 15-23 tak sirf itna sa kar raha h pehle toh......
        try:                                                                                         # ...joh product ki request kar rahe h use find kar 
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Now pass the session_id to cart.    # rahe h then apan ne joh Cart model banaya uska
        except Cart.DoesNotExist:                                                                    # kam ye h ki har user ki cart_id(session_id) voh
            cart = Cart.objects.create(                                                              # voh stroe karke rakhe.toh apan yaha cart_id me 
                cart_id =_cart_id(request)                                                           # voh session_id dal rahe h try me toh agar session_id
            )                                                                                        # nahi h toh simply use create karke dal rahe h
        cart.save()                                                                                  # then save. Hum id ke tor pesession_id consider kar rahe h bss.
                                                                                                    # yaha to simply bss items ko cart_item me add
                                                                                                    # kar rahe h .
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)   
            # existing_variations  --> database
            # current variation    --> product_variation
            # item_id           
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                # create a new cart item
                if len(product_variation) > 0:                                                           
                    item.variations.clear()
                    item.variations.add(*product_variation)                                                                                                                                                
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0: 
                cart_item.variations.clear()                                                         
                cart_item.variations.add(*product_variation)  
            cart_item.save()
        
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
                 # Get the session_id
    product = get_object_or_404(Product, id=product_id)              # Get product_id
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)     # Get the actual product from cart which we want to remove.
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
                # Get the session_id
    product = get_object_or_404(Product, id=product_id)            # Get product_id
    if request.user.is_authenticated:
        car_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        car_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)    # Get the actual product from cart which we want to remove.
    car_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:                                              # For looged-in user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))                      # Get the session_id        For non-logged user
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)         # Get product_id
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):                   # Simple copy-paste the cart() function
    try:                                                                       # Because we need to dislay same cart in right side.
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:                                              # For looged-in user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)   # Taking values from cart page to checkout page (in-else block).
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))                      
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context)

