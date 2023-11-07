from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from marketplace.context_processors import get_cart_counter
from marketplace.models import Cart
from menu.models import Category, Product
from vendor.models import Vendor


def marketplace (request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()

    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'product',
            queryset=Product.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id=product_id)
                try:
                    check_cart = Cart.objects.get(user=request.user,product=product)
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Cart quantity has been increased.',
                                         'cart_counter': get_cart_counter(request), 'qty':check_cart.quantity})
                except:
                    check_cart = Cart.objects.create(user=request.user,product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'The product has been added to the cart.',
                                         'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist.'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue.'})

def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id=product_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, product=product)
                    if check_cart.quantity >1:

                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status': 'Success',
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'This product does not exist in your cart.'})

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist.'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html',context )

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted',
                                         'cart_counter':get_cart_counter(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.', })

