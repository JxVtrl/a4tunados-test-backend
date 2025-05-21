from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Video, Categoria, Playlist
from .permissions import IsProfessorOrReadOnly
from .serializers import RegisterSerializer,UserSerializer,VideoSerializer,CategoriaSerializer,PlaylistSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsProfessorOrReadOnly]

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsProfessorOrReadOnly]

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