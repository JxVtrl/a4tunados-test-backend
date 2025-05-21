from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_CHOICES = (
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

class Playlist(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    videos = models.ManyToManyField('Video', related_name='playlists', blank=True)

    def __str__(self):
        return self.nome

class Video(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='videos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.titulo