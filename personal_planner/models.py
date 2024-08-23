from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from registration.models import Usuario

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100,unique=True, verbose_name='Título del evento')
    description = models.TextField(blank=True, verbose_name='Descripción del evento')
    start_date = models.DateTimeField(verbose_name='Fecha y hora de inicio del evento')
    end_date = models.DateTimeField(verbose_name='Fecha y hora de fin del eventoo')
    location = models.CharField(max_length=200, blank=True, verbose_name='Ubicación')
    is_public = models.BooleanField(default=False, verbose_name='¿Es público?')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, default='', verbose_name='Slug')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'event-{slugify(self.title)}'
        super(Event, self).save(*args, **kwargs)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')

    def __str__(self):
        return self.title 