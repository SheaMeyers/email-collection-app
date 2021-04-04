from django import forms

from app.models import EmailEntry


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailEntry
        fields = ('email',)
