from rest_framework import serializers
from .models import Video, User, Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False)
    foto_url = serializers.SerializerMethodField()
    class Meta:
        model = Playlist
        fields = ['id', 'nome', 'descricao', 'professor', 'videos', 'foto', 'foto_url']
        read_only_fields = ['id', 'professor']

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if obj.foto and request:
            url = request.build_absolute_uri(obj.foto.url)
            # Garante que a porta 8081 está presente
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            return url
        return None

class VideoSerializer(serializers.ModelSerializer):
    playlists = PlaylistSerializer(many=True, read_only=True)
    playlists_ids = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(), many=True, write_only=True, source='playlists'
    )
    arquivo = serializers.FileField(required=True)
    professor_nome = serializers.CharField(source='professor.username', read_only=True)  # Adiciona o nome do professor
    thumbnail = serializers.ImageField(required=False, allow_null=True, use_url=True)  # Adiciona o campo thumbnail
    arquivo_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ['id', 'titulo', 'descricao', 'arquivo', 'arquivo_url', 'criado_em', 'professor', 'professor_nome', 'playlists', 'playlists_ids', 'thumbnail', 'thumbnail_url']
        read_only_fields = ['id', 'criado_em', 'professor', 'playlists', 'thumbnail']

    def get_arquivo_url(self, obj):
        request = self.context.get('request')
        if obj.arquivo and request:
            url = request.build_absolute_uri(obj.arquivo.url)
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            return url
        return None

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            url = request.build_absolute_uri(obj.thumbnail.url)
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            return url
        return None

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