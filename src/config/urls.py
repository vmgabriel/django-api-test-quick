"""
Control of Libraries
"""

# Libraries
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authetication
    path(
        'login',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'refresh_token',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('', include('bills.urls')),
]

if settings.DEBUG:
    # Files upload
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
