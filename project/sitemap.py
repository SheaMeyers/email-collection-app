from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from app.models import Page


class StaticViewSitemap(Sitemap):
    changefreq = "never"

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)


class PagesSitemap(Sitemap):
    changefreq = "always"

    def items(self):
        return Page.objects.exclude(url_pathname='')

    def location(self, item):
        return reverse('email-collect', kwargs={'url_pathname': item.url_pathname})
