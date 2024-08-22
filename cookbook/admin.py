from django.contrib import admin
from .models import Categoty, Ingredient, Unit, Recipe, Quality

# Register your models here.
class CatalogAdmin(admin.ModelAdmin):
    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('name',)

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('name',)

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    #CAMPOS DE SOLO LECTURA
    readonly_fields = ('created_date', 'updated_date') 

    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('title', 'category', 'author', 'updated_date')

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('author','-created_date')

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('title', 'author__username',) 

    #AGREGA UNA BARRA LATERAL DE FILTROS
    list_filter = ('author', 'ingredients')


class QualityAdmin(admin.ModelAdmin):
    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('recipe', 'ingredient', 'unit', 'quantity')

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('recipe',)

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('recipe__title', 'ingredient__name',) 



admin.site.register(Categoty, CatalogAdmin)
admin.site.register(Ingredient, CatalogAdmin)
admin.site.register(Unit, CatalogAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Quality, QualityAdmin)