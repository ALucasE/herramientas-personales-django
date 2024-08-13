from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('title', 'owner', 'priority', 'completed')
    ordering = ('owner','-created_date')
    search_fields = ('title', 'owner__username',)

admin.site.register(Task, TaskAdmin)
