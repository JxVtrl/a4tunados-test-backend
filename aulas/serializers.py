from rest_framework import serializers
from .models import Video, User, Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False) 
    class Meta:
        model = Playlist
        fields = ['id', 'nome', 'descricao', 'professor', 'videos', 'foto']
        read_only_fields = ['id', 'professor']

class VideoSerializer(serializers.ModelSerializer):
    playlists = PlaylistSerializer(many=True, read_only=True)
    playlists_ids = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(), many=True, write_only=True, source='playlists'
    )
    arquivo = serializers.FileField(required=True)
    professor_nome = serializers.CharField(source='professor.username', read_only=True)  # Adiciona o nome do professor
    thumbnail = serializers.ImageField(required=False, allow_null=True, use_url=True)  # Adiciona o campo thumbnail
    
    class Meta:
        model = Video
        fields = ['id', 'titulo', 'descricao', 'arquivo', 'criado_em', 'professor', 'professor_nome', 'playlists', 'playlists_ids', 'thumbnail']
        read_only_fields = ['id', 'criado_em', 'professor', 'playlists', 'thumbnail']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tipo']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'tipo']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            tipo=validated_data['tipo']
        )
        user.is_active = True  # Garante que o usuário está ativo
        user.save()
        return user