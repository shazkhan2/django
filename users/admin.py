from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_editable = ('user_type',)



    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('user_type',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Role', {'fields': ('user_type',)}),
    )

admin.site.register(User, CustomUserAdmin)

