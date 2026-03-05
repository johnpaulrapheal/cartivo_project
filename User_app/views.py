from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User,Cart,CartItem,Order,OrderItem,Wishlist,WishlistItem
from User_app.decorators import customer_login_required,customer_required
from Seller_app.models import Product,ProductImage,ProductVariant,VariantAttributeBridge


# Create your views here.

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get('password')
        profile_image=request.FILES.get('profile_image')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")
        
        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return redirect("register")
        
        data_user = User(username=username,email=email,phone_number=phone_number,password=make_password(password),profile_image=profile_image)
        data_user.save()
        return redirect("login") 
    return render (request,"user/register_user.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()
        if user_obj:
            user = authenticate(request,username=user_obj.username,password=password)
            if user is not None:
                if user_obj.role == 'CUSTOMER':
                    login(request,user)
                    return redirect('home')
                else:
                    messages.error(request,"you are not allowed to login as user")
            else:
                messages.error(request,"invalid username or password")
    return render(request,"user/user_login.html")

@customer_login_required
def user_profile(request):
    user = request.user
    if request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        else:
            messages.success(request, "Username updated")
        
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Email already exists")
            return redirect("register")
        else:
            messages.success(request, "Email updated")
    
        if User.objects.filter(phone_number=phone_number).exclude(id=user.id).exists():
            messages.error(request, "Phone number already exists")
            return redirect("register")
        else:
            messages.success(request, "Phone Number updated")

        user.username=username
        user.email=email
        user.phone_number=phone_number
        user.save()

    return render(request,'user/user_profile.html')

@customer_login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@customer_required
def user_home(request):
    user = request.user
    products = products = Product.objects.filter(is_active=True,approval_status='APPROVED').prefetch_related('variants__images')
    return render(request,'user/home.html',{'products':products})

@customer_login_required
def user_wishlist(request,id):
    user_name=request.user
    variant=ProductVariant.objects.get(id=id)
    wishlist, created=Wishlist.objects.get_or_create(user=user_name)
    wishlist_item=WishlistItem.objects.filter(cart=cart,variant=variant).first()
    if wishlist_item:
            messages.error(request,"item already in your wishlist")
    else:
        add_to_wishlist=WishlistItem(wishlist=wishlist,variant=variant)
        add_to_wishlist.save()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)

@customer_login_required
def user_wishlist_item_delete(request,id):
    variant=ProductVariant.objects.get(id=id)
    Wishlist_item=WishlistItem.objects.get(variant=variant)
    Wishlist_item.delete()
    return redirect('wishlist')

@customer_login_required
def user_wishlist_display(request):    
    user_name=request.user
    wishlist, created=Wishlist.objects.get_or_create(user=user_name)
    wishlist_item=WishlistItem.objects.filter(wishlist=wishlist)
    return render(request,'user/wishlist.html',{'wishlist_item':wishlist_item})

@customer_login_required
def user_cart(request,id):
    user_name=request.user
    variant=ProductVariant.objects.get(id=id)
    cart, created=Cart.objects.get_or_create(user=user_name)
    cart_item=CartItem.objects.filter(cart=cart,variant=variant).first()
    if cart_item:
        if cart_item.quantity <= variant.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            cart.total_amount=cart_item.price_at_time*cart_item.quantity
            cart.total_amount += variant.cost_price
            cart.save()
        else:
            messages.error(request,"item stock out")
    else:
        cart_item=CartItem(cart=cart,variant=variant,quantity=1,price_at_time=variant.cost_price)
        cart_item.save()
        cart.total_amount=variant.cost_price
        cart.save()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)

@customer_login_required
def user_cart_add_quantity(request,id):
    variant=ProductVariant.objects.get(id=id)
    cart=Cart.objects.get(user=request.user)
    cart_item=CartItem.objects.get(variant=variant)
    if cart_item.quantity < variant.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
        cart.total_amount += variant.cost_price
        cart.save()
    else:
        messages.error(request,"item stock out")
    return redirect('cart')

@customer_login_required
def user_cart_substract_quantity(request,id):
    variant=ProductVariant.objects.get(id=id)
    cart=Cart.objects.get(user=request.user)
    cart_item=CartItem.objects.get(variant=variant)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        cart.total_amount -= variant.cost_price
        cart.save()
    else:
        cart_item.delete()
        cart.total_amount -= variant.cost_price
        cart.save()
    return redirect('cart')

@customer_login_required
def user_cart_item_delete(request,id):
    variant=ProductVariant.objects.get(id=id)
    cart_item=CartItem.objects.get(variant=variant)
    cart_item.delete()
    return redirect('cart')

@customer_login_required
def user_cart_display(request):    
    user_name=request.user
    cart=Cart.objects.filter(user=user_name).first()
    cart_item=CartItem.objects.filter(cart=cart)
    return render(request,'user/cart.html',{'cart_item':cart_item,'cart':cart})

@customer_login_required
def user_orders(request):
    return render(request,'user/myorders.html')

@customer_login_required
def user_address(request):
    return render(request,'user/add_address.html')

@customer_login_required
def user_payment_method(request):
    return render(request,'user/payment_add.html')

@customer_login_required
def user_product_view(request,id):
    user=request.user
    variant = ProductVariant.objects.select_related('product').prefetch_related('images').get(id=id)
    variants = ProductVariant.objects.filter(product=variant.product).prefetch_related('images')
    return render(request,'user/product_view.html',{'variant':variant,'variants':variants,'user':user})

@customer_login_required
def user_payment_choice(request):
    return render(request,'user/payment.html')  

@customer_login_required
def user_order_confirmation(request,id):
    user_name=request.user
    variant=ProductVariant.objects.get(id=id)
    order=Order.objects.filter(user=user_name).first()
    product_price=variant.cost_price
    if order:
        order_item=OrderItem.objects.filter(order=order,variant=variant).first()
        if order_item:
            if order_item.quantity < variant.stock_quantity:
                order_item.quantity += 1
                order_item.seller=variant.product.seller
                order_item.save() 
                order.total_amount+=order_item.price_at_purchase
                order.save() 
            else:     
                messages.error(request,"item stock out")
        else:
            order_item1=OrderItem(order=order,variant=variant,seller=variant.product.seller,price_at_purchase=product_price)
            order_item1.save()
    else:
        order1=Order(user=user_name,total_amount=product_price)
        order1.save()
        print(order1.total_amount)
        order_item1=OrderItem(order=order1,variant=variant,seller=variant.product.seller,price_at_purchase=product_price)
        order_item1.save()
    return redirect('user_order_display')

@customer_login_required
def user_order_add_quantity(request,id):
    variant=ProductVariant.objects.get(id=id)
    order=Order.objects.get(user=request.user)
    order_item=OrderItem.objects.get(variant=variant)
    if order_item.quantity < variant.stock_quantity:
        order_item.quantity += 1
        order_item.save()
        order.total_amount += variant.cost_price
        order.save()
    else:
        messages.error(request,"item stock out")
    return redirect('user_order_display')

@customer_login_required
def user_order_substract_quantity(request,id):
    variant=ProductVariant.objects.get(id=id)
    order=Order.objects.get(user=request.user)
    order_item=OrderItem.objects.get(variant=variant)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        order.total_amount -= variant.cost_price
        order.save()
    else:
        order_item.delete()
        order.total_amount -= variant.cost_price
        order.save()
    return redirect('user_order_display')

@customer_login_required
def user_order_item_delete(request,id):
    variant=ProductVariant.objects.get(id=id)
    order_item=OrderItem.objects.get(variant=variant)
    order_item.delete()
    return redirect('user_order_display')

@customer_required
def user_order_display(request):   
    user_name=request.user
    order=Order.objects.filter(user=user_name).first()
    order_item=OrderItem.objects.filter(order=order)
    return render(request,'user/order_confirmation.html',{'order_item':order_item,'order':order})