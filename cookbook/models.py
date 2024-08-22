from django.db import models
from ckeditor.fields import RichTextField
from registration.models import Usuario


# Create your models here.
class Categoty(models.Model):
    '''
    Modelo tipo catalogo
    '''

    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la categoria')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Unit(models.Model):
    '''
    Modelo tipo catalogo
    '''

    name = models.CharField(max_length=100, unique=True, verbose_name='Unidad de medida')

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''
    Modelo tipo catalogo
    '''

    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre del ingrediente')

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=90, unique=True, verbose_name='Titulo')
    description = models.CharField(max_length=200, verbose_name='Descipcion breve')
    ingredients = models.ManyToManyField(Ingredient, through='Quality')
    instructions = RichTextField(verbose_name='Instrucciones')
    image = models.ImageField(
        upload_to='recipe', null=True, blank=True, default='/static/img/cookbook/cookbook-default.png', verbose_name='Imagen'
    )
    category = models.ForeignKey(Categoty, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    author = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def get_ingredients(self):
        return self.ingredients.all()
    
    def get_ingredients_with_quantities(self):
        return self.quality_set.all()
    
    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['title']

    def __str__(self):
        return self.title


class Quality(models.Model):
    '''
    Modelo tipo pivot
    '''

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Receta')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ingrediente')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, verbose_name='Unidad de medida')
    quantity = models.CharField(max_length=10, verbose_name='Catidad')
    notes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nota de observación')

    class Meta:
        verbose_name = 'Cantidad'
        verbose_name_plural = 'Cantidades'

    def __str__(self):
        return (f'Receta: {self.recipe.title} - Ingrediente: {self.ingredient.name}')
