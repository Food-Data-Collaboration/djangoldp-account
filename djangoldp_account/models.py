import validators
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from djangoldp.models import Model


class LDPUser(AbstractUser, Model):
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        rdf_type = 'foaf:user'
        owner_field = 'id'
        lookup_field = 'slug'

    def name(self):
        return self.get_full_name()

    def webid(self):
        # hack : We user webid as username for external user (since it's an uniq identifier too)
        if validators.url(self.username):
            webid = self.username
        else:
            webid = '{0}{1}'.format(settings.BASE_URL, reverse_lazy('ldpuser-detail', kwargs={'pk': self.pk}))
        return webid


class Account(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    picture = models.URLField(blank=True, null=True)
    issuer = models.URLField(blank=True, null=True)

    class Meta:
        auto_author = 'user'
        permissions = (
            ('view_account', 'Read'),
            ('control_account', 'Control'),
        )
        rdf_context = {'picture': 'foaf:depiction'}
        lookup_field = 'slug'

    def __str__(self):
        return '{} ({})'.format(self.user.get_full_name(), self.user.username)


class ChatProfile(Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chatProfile")
    slug = models.SlugField(unique=True)
    jabberID = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        auto_author = 'user'
        permissions = (
            ('view_chatprofile', 'Read'),
            ('control_chatprofile', 'Control'),
        )
        lookup_field = 'slug'

    def __str__(self):
        return '{} (jabberID: {})'.format(self.user.get_full_name(), self.jabberID)


class OPClient(Model):
    issuer = models.URLField()
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)

    def __str__(self):
        return '{} ({})'.format(self.issuer, self.client_id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, slug=instance.username)
        chat_profile = ChatProfile.objects.create(user=instance, slug=instance.username)
        if settings.JABBER_DEFAULT_HOST:
            chat_profile.jabberID = '{}@{}'.format(instance.username, settings.JABBER_DEFAULT_HOST)
            chat_profile.save()
        instance.slug = instance.username
        instance.save()
    else:
        try:
            instance.slug = instance.username
            instance.save()
            instance.account.slug = instance.username
            instance.account.save()
            instance.chatProfile.slug = instance.username
            instance.chatProfile.save()
        except:
            pass
