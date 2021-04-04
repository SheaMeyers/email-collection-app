from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    url_pathname = models.CharField(blank=True, max_length=40)
    title = models.CharField(blank=True, max_length=40)
    sub_title = models.CharField(blank=True, max_length=40)
    text_above_email = models.TextField(blank=True)
    text_below_email = models.TextField(blank=True)
    background_colour = models.CharField(blank=True, max_length=6, help_text='Six character hex value')


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=True,
                                   help_text=_('Designates whether the user can log into this admin site.'),)
    page = models.OneToOneField(Page, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class EmailEntry(models.Model):
    date_added = models.DateTimeField(_('date added'), default=timezone.now)
    email = models.EmailField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='email_entries')
