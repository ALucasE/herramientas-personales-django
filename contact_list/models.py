from django.db import models
from registration.models import Usuario

# Create your models here.
CHOICE_COLOR= (
    ('primary','Orange'),
    ('success','Green'),
    ('info','LightBlue'),
    ('warning','Yelow'),
    ('danger','Red')
)


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __str__(self):
        return self.name 


class Contact(models.Model):
    first_name  = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    phone = models.CharField(max_length=20, verbose_name='Numero de telefono')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo electronico')
    address = models.TextField(null=True, blank=True, verbose_name='Direccion')
    birthdate = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Grupo')
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        if self.address:
            self.address = self.address.upper()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'
    
    
    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name()



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    color = models.CharField(choices=CHOICE_COLOR, max_length=10,verbose_name='Color')
    contacts = models.ManyToManyField(Contact, related_name='tags')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']

    def __str__(self):
        return self.name