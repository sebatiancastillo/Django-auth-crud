from django import forms
from tasks.models import Task  # Asegúrate de que el modelo Task esté definido en tasks/models.py

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Reemplaza 'Task' con el modelo de tu tarea
        fields = ['title', 'description', 'important']  # Especifica los campos que quieres incluir en el formulario

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task Description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),      }  # Personaliza los widgets si es necesario