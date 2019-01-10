from django.contrib import admin
from .models import Account, ChatProfile, ChatConfig


class ChatProfileInline(admin.StackedInline):
    model = ChatProfile


class ChatConfigAdmin(admin.ModelAdmin):
    inlines = [ChatProfileInline]


admin.site.register(ChatConfig, ChatConfigAdmin)
admin.site.register(Account)
