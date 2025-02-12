from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active') # Here is the list what you want to display in admin page superuser information.
    list_display_links = ('email', 'first_name', 'last_name')                                     # Here we want that our email, first_name, last_name when we click it we go to same page same we go to our clicking on email page.
    readonly_fields = ('last_login', 'date_joined')                                               # Here we define read_only fields.
    ordering = ('-date_joined',)                                                                  # Date should be in descending order.

    filter_horizontal = ()                      # These three are mandotory fields.
    list_filter =()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)