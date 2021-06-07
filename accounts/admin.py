from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . forms import  UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    readonly_fields=('date_joined', 'last_login',)

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_admin']
    list_filter = ['is_superuser', 'is_admin', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_staff')}),
        ('Date and Time', {'fields': ('date_joined', 'last_login',)}),
        ('Groups', {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['username']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)