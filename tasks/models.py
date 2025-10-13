from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario de Django

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)  # Título de la tarea
    description = models.TextField(blank=True)  # Descripción de la tarea, puede estar vacía
    created = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la tarea, se establece automáticamente al crear la tarea
    datecompleted = models.DateTimeField(null=True,  blank=True)  # Fecha de finalización de la tarea, puede estar vacía se agrega blank=True
    # Permite que el campo sea opcional, es decir, puede ser nulo o estar en blanco
    important = models.BooleanField(default=False)  # Marca si la tarea es importante, por defecto es False
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Relación con el modelo de usuario, elimina las tareas si el usuario es eliminado


    def __str__(self):
        return self.title + '- by ' + self.user.username  # Representación en cadena de la tarea, muestra el título y el nombre de usuario del creador
    