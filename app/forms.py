from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput

from app.models import EmailEntry, Page


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

        return self.cleaned_data['url_pathname']
