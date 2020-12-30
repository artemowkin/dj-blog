import json

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import LANGUAGE_SESSION_KEY


def set_language(request):
    if request.method == 'POST':
        language = json.loads(request.body).get(
            'language', settings.LANGUAGE_CODE
        )
    else:
        language = request.GET.get(
            'language', settings.LANGUAGE_CODE
        )

    response = JsonResponse({'status': 'ok'})
    if request.user.is_authenticated:
        request.session[LANGUAGE_SESSION_KEY] = language

    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, language,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response
