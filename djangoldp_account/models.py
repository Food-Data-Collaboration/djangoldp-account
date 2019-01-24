from django.contrib.auth.models import User
from django.db import models


def name(self):
    return self.get_full_name()


User.name = name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)

    class Meta:
        auto_author = 'user'
        permissions = (
            ('view_account', 'Read'),
            ('control_account', 'Control'),
        )

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.user.username)


class ChatProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="chatProfile")
    jabberID = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        auto_author = 'user'
        permissions = (
            ('view_chatprofile', 'Read'),
            ('control_chatprofile', 'Control'),
        )

    def __str__(self):
        return '{} (jabberID: {})'.format(self.user.get_full_name(), self.jabberID)
