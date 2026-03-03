from django .urls import path
from .import views

urlpatterns=[
    path('register/',views.user_register,name='register'),
    path('login/',views.user_login,name='login'),
    path('profile/',views.user_profile,name='profile'),
    path('logout/',views.user_logout,name='logout'),
    path('home/',views.user_home,name='home'),
    path('wishlist/',views.user_wishlist,name='wishlist'),
    path('cart/',views.user_cart_display,name='cart'),
    path('myorders/',views.user_orders,name='myorders'),
    path('address/',views.user_address,name='address'),
    path('payment_method/',views.user_payment_method,name='payment_method'),
    path('product_view/<int:id>/',views.user_product_view,name='product_view'),
    path('payment_choice',views.user_payment_choice,name='payment_choice'),
    path('add_cart/<int:id>/',views.user_cart,name='add_cart'),
    path('add_cart_quantity/<int:id>/',views.user_cart_add_quantity,name='add_cart_quantity'),
    path('sub_cart_quantity/<int:id>/',views.user_cart_substract_quantity,name='sub_cart_quantity'),      
    path('delete_cart_item/<int:id>/',views.user_cart_item_delete,name='delete_cart_item'),
    path('user_order_confirm/',views.user_order_confirmation,name='user_order_confirm'),
    path('user_order_display/<int:id>',views.user_order_display,name='user_order_display'),
]       