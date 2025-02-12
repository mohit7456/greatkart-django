from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):                    # Here we define how slug is pehle se he generate ho jae.
    prepopulated_fields = {'slug': ('category_name',)}    # Here we define how our slug field is auto-generated when we write category_name then slug_field is auto_generated.
    list_display = ('category_name', 'slug')              # Here we dsiaplay what we want to display in admin page.
 
admin.site.register(Category, CategoryAdmin)