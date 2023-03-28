from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RoleInline(admin.StackedInline):
    model = User.roles.through
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = (RoleInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'roles_list')

    def roles_list(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

    roles_list.short_description = "Roles"


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
