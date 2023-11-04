from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

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
        if request.is_ajax():
            try:
                product = Product.objects.get(id=product_id)
                try:
                    checkCart = Cart.objects.get(user=request.user,product=product)
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Cart quantity has been increased.'})
                except:
                    checkCart = Cart.objects.create(user=request.user,product=product, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'The product has been added to the cart.'})

            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist.'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request.'})
    else:
        return JsonResponse({'status':'Failed', 'message':'Please login to continue.'})
