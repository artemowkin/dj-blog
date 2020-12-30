import logging

from django.views import View
from django.http import HttpRequest, Http404
from django.core.exceptions import PermissionDenied


logger = logging.getLogger('filelogger')


class DefaultView(View):
    """View with exceptions handling"""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            logger.debug(f"Request on {request.path}")
            return super().dispatch(request, *args, **kwargs)
        except (Http404, PermissionDenied):
            logger.warning(f"404 Not Found on {request.path}")
            raise
        except Exception:
            logger.exception(f"Problem with request on {request.path}")
            raise
