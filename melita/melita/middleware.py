from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class ForceAdminLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info.startswith("/admin/"):
            language = settings.LANGUAGE_CODE
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        response.headers.setdefault("Content-Language", language)
        return response
