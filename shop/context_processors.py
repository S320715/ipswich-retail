"""Context processors for the shop application."""


def cart_count(request):
    """Add cart item count to all template contexts."""
    cart = request.session.get('cart', {})
    count = sum(item.get('quantity', 1) for item in cart.values())
    return {'cart_count': count}
