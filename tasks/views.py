# Importa la función para renderizar plantillas HTML
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
# Formulario de registro de usuario de Django
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout ,  authenticate  # Decorador para proteger vistas que requieren autenticación
# Importa el modelo de usuario de Django para crear nuevos usuarios
from django.contrib.auth.models import User  # Modelo de usuario de Django
#from django.http import HttpResponse  # Permite devolver respuestas HTTP simples
from django.db import IntegrityError  # Importa la excepción IntegrityError para manejar errores de base de datos
from .forms import TaskForm  # Importa el formulario de tarea
from .models import Task  # Importa el modelo de tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required # Decorador para proteger vistas que requieren autenticación


# Aquí se definen las vistas de la aplicación

def signup(request):
    # Vista para el registro de usuarios
    if request.method == 'GET':
        # Si la petición es GET, muestra el formulario de registro
        return render(request, 'signup.html', {
            'form': UserCreationForm  # Pasa el formulario de registro a la plantilla
        })
    else:
        # Si la petición es POST, procesa los datos enviados por el usuario
        if request.POST['password1'] == request.POST['password2']:
            # Verifica que las contraseñas coincidan
            try:
                # Intenta crear un nuevo usuario con el nombre y contraseña proporcionados
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()  # Guarda el usuario en la base de datos
                login(request, user)  # Inicia sesión automáticamente al crear el usuario
                # Redirige al usuario a la página de tareas después del registro exitoso    
                return redirect('tasks')  # Redirige al usuario a la página de tareas
            except IntegrityError:
                # Si ocurre un error interno (por ejemplo, problemas con la base de datos)
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists.'
                })
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Passwords do not match'  # Mensaje de error para el usuario
            })
@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def home(request):
    # Vista para la página principal. Renderiza la plantilla 'home.html'
    return render(request, 'home.html')

@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)  # Filtra las tareas del usuario actual
    # Vista para la página de tareas
    return render(request, 'tasks.html', {'tasks': tasks})  # Renderiza la plantilla 'tasks.html'

@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  # Filtra las tareas del usuario actual
    # Vista para la página de tareas
    return render(request, 'tasks.html', {'tasks': tasks})  # Renderiza la plantilla 'tasks.html'
    
@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def create_task(request):
    if request.method == 'GET': # Vista para crear una nueva tarea
        return render(request, 'create_task.html', {
        'form': TaskForm  # Pasa el formulario de tarea a la plantilla
    })
    else : 
        try:
            # Si la petición es POST, crea una nueva tarea con los datos del formulario
            form = TaskForm(request.POST)  # Crea una instancia del formulario con los datos enviados
            new_task = form.save(commit=False)  # No guarda aún en la base de datos
            new_task.user = request.user  # Asigna el usuario actual a la tarea
            new_task.save()  # Guarda la tarea en la base de datos
            return redirect('tasks')  # Redirige al usuario a la página de tareas después de crear la tarea     
        except ValueError:
            # Si ocurre un error al guardar la tarea (por ejemplo, datos inválidos)
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Error creating task. Please try again.'  # Mensaje de error para el usuario
            })
@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  # Obtiene la tarea por su ID
        form = TaskForm(instance=task)  # Crea una instancia del formulario de tarea con la tarea existente
        return render(request, 'task_detail.html', {'task': task, 'form': form})  # Renderiza la plantilla 'task_detail.html' con la tarea y el formulario
    else:

        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)  # Asegura que la tarea pertenece al usuario actual
            form = TaskForm(request.POST, instance=task)  # Crea una instancia del formulario con los datos enviados y la tarea existente
            form.save()  # Guarda los cambios en la tarea
            return redirect('tasks')  # Redirige al usuario a la página de tareas después de actualizar la tarea
           # Si la petición es POST, actualiza la tarea con los datos del formulario
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task. Please try again.'  # Mensaje de error para el usuario
            })

@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Asegura que la tarea pertenece al usuario actual
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')    

@login_required # Protege la vista para que solo usuarios autenticados puedan acceder
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Asegura que la tarea pertenece al usuario actual
    if request.method == 'POST':
        task.delete()  # Elimina la tarea de la base de datos
        return redirect('tasks')  # Redirige a la página de tareas después de eliminar la tarea
    # Si la petición es POST, marca la tarea como completada

def signout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('signin')  # Redirige a la página de inicio de sesión

def signin(request): 
    if request.method == 'GET':
        return render(request, 'signin.html',
                  {'form': AuthenticationForm()
                   })  # Renderiza la plantilla 'signin.html'
# Esta vista podría ser utilizada para iniciar sesión, pero no está implementada en este código.
    else:
        user =  authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'El nombre de usuario o la contraseña son incorrectos'
            })   
        else:
            login(request, user)
            return redirect('tasks')
        # Si la petición es POST, intenta autenticar al usuario
        # Si la autenticación falla, muestra un mensaje de error
        # 
        #      
        return render(request, 'signin.html',
                  {'form': AuthenticationForm()
                   })  # Renderiza la plantilla 'signin.html'
# Esta vista podría ser utilizada para iniciar sesión, pero no está implementada en este código.