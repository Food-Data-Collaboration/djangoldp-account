from django.contrib import admin
from .models import Account, ChatProfile, ChatConfig

admin.site.register(Account)
admin.site.register(ChatConfig)
admin.site.register(ChatProfile)
