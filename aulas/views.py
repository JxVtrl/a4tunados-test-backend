from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Video, Playlist
from .permissions import IsProfessorOrReadOnly
from .serializers import RegisterSerializer,UserSerializer,VideoSerializer,PlaylistSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsProfessorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)

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