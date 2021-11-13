from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'phone',  'is_assistant', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        ('user_info', {'fields': ('username', 'name', 'family', 'phone', 'email', 'password')}),
        ('personal_info', {'fields': ('is_active', 'is_assistant')}),
        ('permissions', {'fields': ('is_admin',)})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'password1', 'password2')}),
    )
    search_fields = ('email', 'username', 'phone')
    ordering = ('email', 'username')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


admin.site.unregister(Group)

