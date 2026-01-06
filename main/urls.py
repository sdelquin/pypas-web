from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('', lambda _: redirect(settings.PYPAS_DOCS_URL)),
    path('docs/', lambda _: redirect(settings.PYPAS_DOCS_URL)),
    path('__reload__/', include('django_browser_reload.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('admin/', include('exercises.urls_admin')),
    path('admin/', include('chunks.urls_admin')),
    path('admin/', admin.site.urls),
    path('exercises/', include('exercises.urls')),
    path('access/', include('access.urls')),
    path('assignments/', include('assignments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
