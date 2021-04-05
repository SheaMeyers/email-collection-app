from django import forms
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
