from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, Crypto

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('nickname', 'email', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'password1', 'password2',)}
         ),
    )
    search_fields = ('email','nickname',)
    ordering = ('email','nickname',)
    filter_horizontal = ()


class CryptoAdmin(admin.ModelAdmin):
    list_display = ('id','user','crypto_currency','api_name', 'api_key', 'api_secret',)
    search_fields = ('id','user',)

admin.site.register(Crypto, CryptoAdmin)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
