"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from myapp import views

# for media_root
from django.conf import settings
from django.conf.urls.static import static

# rest framework
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home_page, name="home-page"),
    path('products/', views.ProductList.as_view()),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("showDetails/", views.show_details, name="showDetails"),
    path("add_product/", views.add_product, name="add_product"),
    path("EditProduct/<int:pid>", views.edit_product, name="EditProduct"),
    path("DeleteProduct/<int:pid>", views.delete_product, name="DeleteProduct"),
    path("UpdateProduct/<int:pid>", views.update_product, name="UpdateProduct"),
    path("product/", views.products, name='products'),
    path("users/", views.users, name='users'),
    path("suppliers/", views.suppliers, name='suppliers'),
    path("billing/", views.make_bill, name="billing"),
    path("customer_receipt/", views.customer_receipt, name="customerReceipt"),
    path("deduct_qty/", views.deduct_qty, name="deduct-qty"),
    path("updated_products/", views.updated_products, name="updated_products"),
    path("billing-qrcode/", views.qrcode_billing, name="QrcodeBilling"),
    path("qty-price/", views.get_qty_and_price, name="qty_and_price"),
    path("get_supplier_info/", views.auto_fill_supplier_info, name="auto_fill_supplier_info"),
    path("get_product_details/", views.get_product_details, name="get_product_details"),
    path("customer_details/", views.customer_details, name="customer_details"),
    path("reports/", views.reports, name="reports"),
    path("curd/", views.curd, name="curd"),
    path("add/", views.add, name="add"),
    path("insert/", views.insert, name="insert"),
    # for getting details of std having id on curd
    path('curd/<int:sid>', views.details),
    path('delete/<int:sid>', views.std_delete),
    path('update/<int:sid>', views.update),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)