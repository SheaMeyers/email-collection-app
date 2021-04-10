import re

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms.widgets import TextInput
from django.template import loader
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.models import EmailEntry, Page, User


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailEntry
        fields = ('email',)


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'background_colour': TextInput(attrs={'type': 'color'}),
        }
        fields = '__all__'

    def clean_url_pathname(self):
        if self.cleaned_data['url_pathname'] and self.instance.url_pathname != self.cleaned_data['url_pathname'] and \
                Page.objects.filter(url_pathname=self.cleaned_data['url_pathname']).exists():
            raise ValidationError(f"Another page already has the url path name {self.cleaned_data['url_pathname']}")

        if self.cleaned_data['url_pathname'] in ['sign-up', 'guide', 'admin', 'auth', 'sitemap.xml', 'robots.txt']:
            raise ValidationError(f"Another page already has the url path name {self.cleaned_data['url_pathname']}")

        if self.cleaned_data['url_pathname'] and not re.match('^[A-Za-z0-9_-]*$', self.cleaned_data['url_pathname']):
            raise ValidationError(f"Url pathname can only contain letters, numbers, dashes, and underscores")

        return self.cleaned_data['url_pathname']


class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=254,)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        return email_message.send()

    def save(self, request=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        if User.objects.filter(email=email).exists():
            protocol = 'https' if request.is_secure() else 'http',
            reset_password_url = f'<a href={protocol}://{domain}{reverse_lazy("password_reset")}>Click Here</a>'
            messages.error(request, f'Email already exists in our system.  '
                                    f'Please {reset_password_url} if you need to reset your password.')
            return

        page = Page.objects.create()
        user = User.objects.create(email=email, page=page)

        context = {
            'email': email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        return self.send_mail('sign_up_subject.txt', 'sign_up_email.html', context, settings.EMAIL_HOST_USER, email)
