from decimal import Decimal
"""Views for the shop application."""

import json
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Product

logger = logging.getLogger('shop')


def home(request):
    """Homepage view — shows featured products."""
    featured_products = Product.objects.filter(featured=True)[:6]
    logger.info('Homepage accessed')
    return render(request, 'home.html', {
        'featured_products': featured_products,
    })


def product_list(request):
    """Product listing view — shows all products with optional category filter."""
    products = Product.objects.all()
    category_filter = request.GET.get('category', 'all')

    if category_filter and category_filter != 'all':
        products = products.filter(category=category_filter)

    categories = Product.CATEGORY_CHOICES
    logger.info(f'Product list accessed, category filter: {category_filter}')

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
    })


def product_detail(request, pk):
    """Product detail view — shows full details of one product."""
    product = get_object_or_404(Product, pk=pk)

    # Get related products (same category, exclude current)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:3]

    logger.info(f'Product detail accessed: {product.name} (ID: {pk})')

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def cart_view(request):
    """Shopping cart view — shows all items in session cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = item_data.get('quantity', 1)
            size = item_data.get('size', '')
            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'size': size,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    shipping = 0 if total >= 30 else 3.99
    grand_total = total + Decimal(str(shipping))

    logger.info(f'Cart viewed: {len(cart_items)} items, total: £{grand_total}')

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'subtotal': total,
        'shipping': shipping,
        'total': grand_total,
    })


@require_POST
def add_to_cart(request, pk):
    """Add a product to the session cart."""
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    size = request.POST.get('size', '')
    quantity = int(request.POST.get('quantity', 1))

    product_key = str(pk)

    if product_key in cart:
        cart[product_key]['quantity'] += quantity
        if size:
            cart[product_key]['size'] = size
    else:
        cart[product_key] = {
            'quantity': quantity,
            'size': size,
        }

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f'"{product.name}" added to your cart!')
    logger.info(f'Added to cart: {product.name}, size: {size}, qty: {quantity}')

    return redirect('product_detail', pk=pk)


@require_POST
def remove_from_cart(request, pk):
    """Remove an item from the cart."""
    cart = request.session.get('cart', {})
    product_key = str(pk)

    if product_key in cart:
        del cart[product_key]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item removed from your cart.')
        logger.info(f'Removed from cart: product ID {pk}')

    return redirect('cart')


@require_POST
def update_cart(request, pk):
    """Update the quantity of an item in the cart."""
    cart = request.session.get('cart', {})
    product_key = str(pk)

    if product_key in cart:
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
        except (json.JSONDecodeError, ValueError):
            quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[product_key]['quantity'] = quantity
        else:
            del cart[product_key]

        request.session['cart'] = cart
        request.session.modified = True
        logger.info(f'Updated cart: product ID {pk}, new qty: {quantity}')

    return redirect('cart')
