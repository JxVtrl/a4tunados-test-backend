from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Video, Playlist, User
from .permissions import IsProfessorOrReadOnly
from .serializers import RegisterSerializer,UserSerializer,VideoSerializer,PlaylistSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
import os
import subprocess
from django.conf import settings

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

    def get_queryset(self):
        user = self.request.user
        queryset = Playlist.objects.all()
        if user.is_authenticated and getattr(user, 'tipo', None) == 'professor':
            queryset = queryset.filter(professor=user)
        professor_id = self.request.query_params.get('professor')
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        return queryset

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
        video = serializer.save(professor=self.request.user)
        # Geração automática de thumbnail usando ffmpeg
        if video.arquivo:
            video_path = video.arquivo.path
            thumb_name = f"thumb_{video.id}.jpg"
            thumb_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumb_name)
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            # Comando ffmpeg: pega um frame no segundo 1
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', '00:00:01.000',
                '-vframes', '1',
                '-vf', 'scale=480:-1',
                thumb_path
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Salva o caminho da thumbnail no modelo
                video.thumbnail.name = f'thumbnails/{thumb_name}'
                video.save(update_fields=['thumbnail'])
            except Exception as e:
                print(f'Erro ao gerar thumbnail: {e}')

    def get_queryset(self):
        user = self.request.user
        queryset = Video.objects.all()
        if user.is_authenticated and getattr(user, 'tipo', None) == 'professor':
            # Professor vê apenas seus próprios vídeos
            queryset = queryset.filter(professor=user)
        # Filtro por professor na query string
        professor_id = self.request.query_params.get('professor')
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        return queryset
    
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

class ProfessoresListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        professores = User.objects.filter(tipo='professor')
        serializer = UserSerializer(professores, many=True)
        return Response(serializer.data)