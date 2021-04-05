from django.views.generic import DetailView

from app.models import Page


class EmailCollectView(DetailView):
    model = Page
    slug_field = 'url_pathname'
    slug_url_kwarg = 'url_pathname'
    template_name = 'email_collect.html'
