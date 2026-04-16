"""
URL configuration for cartivo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('user/',include("User_app.urls")),
    path('seller/',include("Seller_app.urls")),
    path('admin_app/', include('Admin_app.urls')),
    
    # Backward-compatible seller links used in templates (without /seller/ prefix)
    path('slogin/', RedirectView.as_view(url='/seller/slogin/', permanent=False)),
    path('regis/', RedirectView.as_view(url='/seller/regis/', permanent=False)),
    path('slogout/', RedirectView.as_view(url='/seller/slogout/', permanent=False)),
    path('sellerhome/', RedirectView.as_view(url='/seller/sellerhome/', permanent=False)),
    path('sellerdashboard/', RedirectView.as_view(url='/seller/sellerdashboard/', permanent=False)),
    path('sellerprofile/', RedirectView.as_view(url='/seller/sellerprofile/', permanent=False)),
    path('sellerproduct/', RedirectView.as_view(url='/seller/sellerproduct/', permanent=False)),
    path('sellerproductview/<slug:slug>', RedirectView.as_view(url='/seller/sellerproductview/%(slug)s', permanent=False)),
    path('sellerproductupdate/<int:id>/', RedirectView.as_view(url='/seller/sellerproductupdate/%(id)s/', permanent=False)),
    path('sellerproductupdate/<int:id>', RedirectView.as_view(url='/seller/sellerproductupdate/%(id)s/', permanent=False)),
    path('sellerimage/<int:id>/', RedirectView.as_view(url='/seller/sellerimage/%(id)s/', permanent=False)),
    path('sellerimage/<int:id>', RedirectView.as_view(url='/seller/sellerimage/%(id)s/', permanent=False)),
    path('togglestatus/<slug:slug>', RedirectView.as_view(url='/seller/togglestatus/%(slug)s', permanent=False)),
    path('sellerorder/', RedirectView.as_view(url='/seller/sellerorder/', permanent=False)),
    path('sellerinactive/', RedirectView.as_view(url='/seller/sellerinactive/', permanent=False)),
    path('sellerreturn/', RedirectView.as_view(url='/seller/sellerreturn/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
