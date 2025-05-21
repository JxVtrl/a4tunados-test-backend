from rest_framework import serializers
from .models import Video, User, Categoria, Playlist

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'nome', 'descricao', 'professor', 'videos']
        read_only_fields = ['id', 'professor']

class VideoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False)
    arquivo = serializers.FileField(required=True)
    playlists = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(), many=True, required=False)

    class Meta:
        model = Video
        fields = ['id', 'titulo', 'descricao', 'arquivo', 'criado_em', 'professor', 'categoria', 'categoria_id', 'playlists']
        read_only_fields = ['id', 'criado_em', 'professor', 'categoria']

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