from django.urls import path
from . import views
urlpatterns =[
    path("slogin/",views.sellerlogin, name='sellerlogin'),
    path("regis/",views.selleregis, name='selleregis'),
    path("sellerhome/",views.sellerhome, name='sellerhome'),
    path("sellerprofile/",views.sellerprofile, name='sellerprofile'),
    path("slogout/",views.seller_logout, name='sellerlogout'),
    path("sellerproduct/",views.sellerproduct, name='sellerproduct'),
    path("sellerproductupdate/<int:id>/", views.sellerproduct_update, name='sellerproductupdate'),
    path("sellerimage/<int:id>/",views.sellerimage, name='sellerimage'),
    path("imagedelete/<int:id>/",views.imagedelete, name='imagedelete'),
    path("selleratribute/",views.selleratribute, name='sellerattribute'),
    path("delete-option/<int:id>/", views.delete_option, name='delete_option'),
    path("sellerproductview/<str:slug>",views.productsingle, name='sellerproductview'),
    path("sellerorder/",views.sellerorder, name='sellerorder'),
    path("togglestatus/<str:slug>",views.toggleproductstatus, name='togglestatus'),
    path("sellerinactive/",views.sellerinactive, name='sellerinactive'),
    path("sellerreturn/",views.sellerreturns, name='sellerreturn'),
    path("sellerdashboard/",views.sellerdashboard, name='sellerdashboard'),

]