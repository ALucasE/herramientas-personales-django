from django.contrib import admin
from .models import Usuario
# Register your models here.

#Default: Administracion de Django
admin.site.site_header = 'Administracion de Herramientas Personales'

#Default: Sitio administrativo
admin.site.index_title = 'Panel de control'

#Default: Sitio administrativo
admin.site.site_title = 'Herramientas Personales'

class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', 'last_login', 'updated') 
    list_display = ('username','is_active','is_staff')
    ordering = ('-date_joined',)
    search_fields = ('username',) 

admin.site.register(Usuario, UsuarioAdmin)