from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),

    # i18n
    path('i18n/', include('langs.urls')),

    # Local
    path('posts/', include('posts.urls')),
]
