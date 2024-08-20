from django.contrib import admin
from .models import Contact, Group, Tag

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    #CAMPOS DE SOLO LECTURA
    readonly_fields = ('created_date', 'updated_date') 

    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('last_name', 'first_name','phone','get_full_name')

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('last_name', 'first_name',)

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('last_name', 'first_name',)

    #AGREGA UNA BARRA LATERAL DE FILTROS
    list_filter = ('last_name', 'group',) 


class GroupAdmin(admin.ModelAdmin):
    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('name',)

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('name',)

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('name',)

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('name',)

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('name',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Tag, TagAdmin)