from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')     # iska mtlb jese apan save kare toh abject ki jagah ye saari fields display ho jae.
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)                                                                     # Here we also tell that which coloris available on stock or not.
    list_filter = ('product', 'variation_category', 'variation_value')                                 # Herewe add a right side section that all items is visible.

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)