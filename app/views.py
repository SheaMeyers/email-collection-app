from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, FormView
from django.urls import reverse_lazy

from app.forms import EmailForm, SignUpForm
from app.models import Page, EmailEntry


class EmailCollectView(FormMixin, DetailView):
    model = Page
    slug_field = 'url_pathname'
    slug_url_kwarg = 'url_pathname'
    template_name = 'email_collect.html'
    form_class = EmailForm

    def get_success_url(self):
        return reverse_lazy('email-collect', kwargs={'url_pathname': self.object.url_pathname})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Email successfully submitted!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        EmailEntry.objects.create(email=form.cleaned_data['email'], page=self.object)
        return super(EmailCollectView, self).form_valid(form)


class SignUpView(FormView):
    template_name = 'sign_up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('sign-up')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        messages.success(self.request, 'Email successfully submitted! Please check your inbox.')
        return super().form_valid(form)
