from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_CHOICES = (
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

class Video(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    link = models.URLField()
    criado_em = models.DateTimeField(auto_now_add=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')