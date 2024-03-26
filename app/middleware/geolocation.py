import geoip2.database
import logging
from django.http import HttpResponseForbidden

class GeolocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR', '')
        user_country = self.get_country_from_ip(user_ip)
        print(user_country)

        if user_country is not None:
            return HttpResponseForbidden("Access restricted to PT-based users only.")

        response = self.get_response(request)
        return response

    def get_country_from_ip(self, ip):
        # Path to your GeoLite2 Country database
        db_path = 'path/to/your/GeoLite2-Country.mmdb'
        try:
            with geoip2.database.Reader(db_path) as reader:
                response = reader.country(ip)
                country = response.country.iso_code
                return country
        except Exception as e:
            logger = logging.getLogger('django')
            logger.debug(e)
            pass
        return None
