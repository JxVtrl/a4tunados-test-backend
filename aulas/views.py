from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Video, Playlist
from .permissions import IsProfessorOrReadOnly
from .serializers import RegisterSerializer,UserSerializer,VideoSerializer,PlaylistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Garante que só remove e seta cookies se access e refresh estiverem presentes
        if response.status_code == 200 and 'access' in response.data and 'refresh' in response.data:
            data = response.data
            response.set_cookie(
                'access_token',
                data['access'],
                max_age=3600,
                httponly=True,
                samesite='Lax',
                secure=False
            )
            response.set_cookie(
                'refresh_token',
                data['refresh'],
                max_age=604800,
                httponly=True,
                samesite='Lax',
                secure=False
            )
            del response.data['access']
            del response.data['refresh']
        return response
    
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsProfessorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)
        
    def perform_update(self, serializer):
        playlist = self.get_object()
        if playlist.professor != self.request.user:
            raise PermissionError("Você não tem permissão para editar esta playlist.")
        serializer.save()

    @action(detail=True, methods=['get'], url_path='videos')
    def videos(self, request, pk=None):
        playlist = self.get_object()
        videos = playlist.videos.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsProfessorOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['criado_em', 'titulo']
    search_fields = ['titulo', 'descricao']

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, 'tipo', None) == 'professor':
            # Professor vê apenas seus próprios vídeos
            return Video.objects.filter(professor=user)
        # Aluno vê todos os vídeos cadastrados (ou pode filtrar por lógica de acesso)
        return Video.objects.all()
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # Permite acesso público


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if 'refresh' not in request.data:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                request.data['refresh'] = refresh_token
        try:
            response = super().post(request, *args, **kwargs)
            # Atualiza o cookie access_token se refresh for bem-sucedido
            if response.status_code == 200 and 'access' in response.data:
                response.set_cookie(
                    'access_token',
                    response.data['access'],
                    max_age=3600,
                    httponly=True,
                    samesite='Lax',
                    secure=False
                )
                del response.data['access']
            return response
        except (TokenError, Exception):
            return Response({'detail': 'Token inválido ou usuário não existe.'}, status=status.HTTP_401_UNAUTHORIZED)