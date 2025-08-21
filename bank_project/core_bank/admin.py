from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Transaction, Service, ServicePayment

# Permite que 'balance' y 'dni' sean editables en el admin de usuario
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('dni', 'balance')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('dni', 'balance')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'dni', 'balance', 'is_staff')
    search_fields = ('username', 'email', 'dni', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction)
admin.site.register(Service)
admin.site.register(ServicePayment)

