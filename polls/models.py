from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from registration.models import Usuario

# Create your models here.
class Poll(models.Model):
    title= models.CharField(max_length=150, verbose_name='Titulo de la Encuesta')
    question_text = models.CharField(max_length=200, verbose_name='Pregunta')
    creator = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')
    

    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        ordering = ['pub_date']

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE,)
    choice_text = models.CharField(max_length=200, verbose_name='Opción')
    votes = models.IntegerField(default=0, verbose_name='Cantidad de votos')
    voters = models.ManyToManyField(Usuario, through='Vote')

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['choice_text']

    def add_vote(self, user):
            # Verificar si el usuario ya ha votado por esta opción
            if Vote.objects.filter(user=user, choice=self).exists():
                raise ValueError("Este usuario ya ha votado por esta opción.")
            
            # Crear un nuevo registro de voto
            Vote.objects.create(user=user, choice=self)
            # Incrementar el conteo de votos
            self.votes += 1
            self.save()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de votación')

    class Meta:
        unique_together = ('user', 'choice')
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'