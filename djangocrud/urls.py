"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Importa el módulo de administración de Django 
from django.urls import path # Importa la función path para definir rutas de URL  
from tasks import views # Importa las vistas de la aplicación 'tasks' 
urlpatterns = [     
    path('admin/', admin.site.urls), # Ruta para el panel de administración de Django
    path('', views.home, name='home'), # Ruta para la página principal en la raíz
    path('signup/', views.signup, name='signup'), # Ruta para el registro de usuarios
    path('tasks/', views.tasks, name='tasks'), # Ruta para ver las tareas
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'), # Ruta para ver las tareas completadas
    path('tasks/create/', views.create_task, name='create_task'),  # Ruta para crear una tarea
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),  # Ruta para editar una tarea
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),  # Ruta para completar una tarea
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),  # Ruta para eliminar una tarea
    path('base/', views.home, name='base'), # Ruta para la plantilla base
    path('logout/', views.signout, name='logout'),  # Ruta para cerrar sesión
    path('signin/', views.signin, name='signin'),  # Ruta para iniciar sesión

]