from rest_framework import serializers
from .models import Video, User, Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, use_url=True)
    class Meta:
        model = Playlist
        fields = ['id', 'nome', 'descricao', 'professor', 'videos', 'foto']
        read_only_fields = ['id', 'professor']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.foto and request:
            url = request.build_absolute_uri(instance.foto.url)
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            data['foto'] = url
        return data

class VideoSerializer(serializers.ModelSerializer):
    playlists = PlaylistSerializer(many=True, read_only=True)
    playlists_ids = serializers.PrimaryKeyRelatedField(
        queryset=Playlist.objects.all(), many=True, write_only=True, source='playlists'
    )
    arquivo = serializers.FileField(required=True, use_url=True)
    professor_nome = serializers.CharField(source='professor.username', read_only=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Video
        fields = ['id', 'titulo', 'descricao', 'arquivo', 'criado_em', 'professor', 'professor_nome', 'playlists', 'playlists_ids', 'thumbnail']
        read_only_fields = ['id', 'criado_em', 'professor', 'playlists', 'thumbnail']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.arquivo and request:
            url = request.build_absolute_uri(instance.arquivo.url)
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            data['arquivo'] = url
        if instance.thumbnail and request:
            url = request.build_absolute_uri(instance.thumbnail.url)
            if ':8081' not in url:
                url = url.replace('api.majorssolutions.com.br', 'api.majorssolutions.com.br:8081')
            data['thumbnail'] = url
        return data

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