from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    #CAMPOS DE SOLO LECTURA
    readonly_fields = ('created_date', 'updated_date', 'slug') 

    #CAMPOS QUE MUESTRAN EN LA LISTA
    list_display = ('title', 'user', 'is_public', 'start_date', 'end_date')

    #COMO SE ORDENAN LOS CAMPOS
    ordering = ('user','-start_date')

    #AGREGA UNA BARRA SUPERIOR DE BUSQUEDA
    search_fields = ('title', 'user__username',) 

    #AGREGA UNA BARRA LATERAL DE FILTROS
    list_filter = ('title', 'is_public')


admin.site.register(Event, EventAdmin)