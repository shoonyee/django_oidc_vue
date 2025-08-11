from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
]

# Add OIDC URLs only in production mode
if getattr(settings, 'MODE', 'LOCAL') == 'PROD':
    urlpatterns.insert(1, path('oidc/', include('mozilla_django_oidc.urls')))
    print("🔐 OIDC URLs enabled for production mode")
else:
    print("🔧 OIDC URLs disabled for local mode")
