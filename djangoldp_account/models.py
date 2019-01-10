from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)

    class Meta:
        permissions = (
            ('view_account', 'Read'),
            ('control_account', 'Control'),
        )

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.user.username)


class ChatConfig(models.Model):
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta:
        permissions = (
            ('view_chatroom', 'Read'),
            ('control_chatroom', 'Control'),
        )

    def __str__(self):
        return '{} ({})'.format(self.jabberID, self.jabberRoom)


class ChatProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="chatProfile")
    config = models.OneToOneField(ChatConfig)

    class Meta:
        permissions = (
            ('view_chatprofile', 'Read'),
            ('control_chatprofile', 'Control'),
        )

    def __str__(self):
        return '{} (jabberID: {})'.format(self.user.get_full_name(), self.config.jabberID)



