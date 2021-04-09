import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    url_pathname = models.CharField(blank=True, max_length=40)
    title = models.CharField(blank=True, max_length=60)
    sub_title = models.CharField(blank=True, max_length=80)
    text_above_email = models.TextField(blank=True)
    text_below_email = models.TextField(blank=True)
    background_colour = models.CharField(blank=True, max_length=7)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.url_pathname and Page.objects.filter(url_pathname=self.url_pathname).exclude(id=self.id).exists():
            raise ValueError(f"Another page already has the url path name {self.url_pathname}")

        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(_('date added'), default=timezone.now)
    email = models.EmailField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='email_entries')


class PasswordCreateRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
