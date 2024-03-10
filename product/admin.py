from django.contrib import admin

from .models import Material, Product, ProductMaterial, Warehouse

admin.site.register(Product)
admin.site.register(Material)
admin.site.register(ProductMaterial)
admin.site.register(Warehouse)
