from Core_app.models import Category
from django.db.models import Sum

from .models import Cart

def category_list(request):
    return {
        "cat": Category.objects.all()
    }


def cart_summary(request):
    cart_total = 0
    cart_count = 0

    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        cart = Cart.objects.filter(user=user).only("id", "total_amount").first()
        if cart:
            cart_total = cart.total_amount or 0
            cart_count = (
                cart.items.aggregate(total=Sum("quantity")).get("total") or 0
            )

    return {
        "cart_total": cart_total,
        "cart_count": cart_count,
    }