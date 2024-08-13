from django.db import models
from django.core.exceptions import ValidationError
from registration.models import Usuario

# Create your models here.

PRIORITY_CHOICES = [
    ('L', 'Low-Baja'),
    ('M', 'Medium-Media'),
    ('H', 'High-Alta'),
]


class Task(models.Model):
    title= models.CharField(max_length=100, verbose_name='Titulo')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    completed = models.BooleanField(default=False, verbose_name='Completado')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M', verbose_name='Prioridad')
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    
    class Meta:
        verbose_name = 'Lista de tarea'
        verbose_name_plural = 'Listas de tareas'
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def is_completed(self):
        return self.completed

    @classmethod
    def get_pending_tasks(cls):
        return cls.objects.filter(completed=False)
