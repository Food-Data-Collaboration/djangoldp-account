from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from djangoldp.admin import DjangoLDPUserAdmin
from djangoldp_account.models import LDPUser


class LDPUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = LDPUser


class LDPUserAdmin(DjangoLDPUserAdmin):
    form = LDPUserChangeForm

    fieldsets = DjangoLDPUserAdmin.fieldsets + (
        (None, {'fields': ('slug', 'default_redirect_uri')}),
    )
    add_fieldsets = DjangoLDPUserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )


admin.site.register(LDPUser, LDPUserAdmin)
