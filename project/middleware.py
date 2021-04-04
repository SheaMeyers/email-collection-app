from django.conf import settings

from django.contrib.gis.geoip2 import GeoIP2

geo_ip2 = GeoIP2()


class IsEuUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            request.is_eu_user = self.is_user_in_EU(request)
        except Exception:
            request.is_eu_user = True

        response = self.get_response(request)

        return response

    def is_user_in_EU(self, request):
        country_code = self.get_user_country_code(request)
        return country_code in settings.EU_COUNTRY_CODES

    def get_user_country_code(self, request):
        ip_address = self.get_user_ip(request)
        country_info = geo_ip2.country(ip_address)
        return country_info['country_code']

    def get_user_ip(self, request):
        # https://stackoverflow.com/a/4581997
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
