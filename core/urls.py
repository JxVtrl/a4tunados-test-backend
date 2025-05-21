from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from aulas.views import VideoViewSet, RegisterView, MeView, CategoriaViewSet, PlaylistViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('api/user/me/', MeView.as_view(), name='me'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)