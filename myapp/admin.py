from django.contrib import admin
from .models import Product, Supplier,Billing, Students
# Register your models here.

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Billing)
admin.site.register(Students)
