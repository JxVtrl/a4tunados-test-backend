from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from aulas.views import VideoViewSet, RegisterView, MeView, PlaylistViewSet, CustomTokenObtainPairView, CookieTokenRefreshView, ProfessoresListView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

schema_view = get_schema_view(
   openapi.Info(
      title="a4tunados API",
      default_version='v1',
      description="Documentação da API da plataforma de aulas para músicos",
      contact=openapi.Contact(email="seu@email.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/me/', MeView.as_view(), name='me'),
    path('api/professores/', ProfessoresListView.as_view(), name='professores-list'),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)