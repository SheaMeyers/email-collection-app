from unittest.mock import patch

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from .forms import SignUpForm
from .models import Page, User, EmailEntry


class SignUpFormTests(TestCase):

    @patch('app.forms.SignUpForm.send_mail')
    def test_form_send_email(self, send_mail_mock):
        form_data = {'email': 'test@email.com'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        request = HttpRequest()
        request.META = {
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8000",
        }
        form.save(request=request)
        send_mail_mock.assert_called_once()

    @patch('django.contrib.messages.api.add_message')
    @patch('app.forms.SignUpForm.send_mail')
    def test_form_no_send_email_when_user_exists(self, send_mail_mock, add_message_mock):
        email = 'test@email.com'
        page = Page.objects.create()
        User.objects.create(email=email, page=page)
        request = HttpRequest()
        request.META = {
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8000",
        }
        form_data = {'email': email}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save(request=request)
        add_message_mock.assert_called_once()
        send_mail_mock.assert_not_called()


class EmailFormTests(TestCase):

    def test_form_send_email(self):
        email = 'test@email.com'
        data = {'email': email}
        page = Page.objects.create(url_pathname='test')
        response = self.client.post(reverse('email-collect',
                                            kwargs={'url_pathname': page.url_pathname}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EmailEntry.objects.filter(email=email).exists())


class HomePageTests(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/admin/login')
        self.assertContains(response, '/sign-up')
