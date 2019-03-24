from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        chat_profile = ChatProfile.objects.create(user=instance)
        if settings.JABBER_DEFAULT_HOST:
            chat_profile.jabberID = '{}@{}'.format(instance.username, settings.JABBER_DEFAULT_HOST)
            chat_profile.save()
    else:
        instance.account.save()
