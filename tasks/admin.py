from django.contrib import admin
from .models import Task  # Importa el modelo Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)  # Campos que se rellenan automáticamente y no se pueden editar en el admin

# Register your models here.
admin.site.register(Task, TaskAdmin)  # Registra el modelo Task con su configuración personalizada
