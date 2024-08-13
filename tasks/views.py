from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm
from .models import Task

# Create your views here.
@login_required
def get_all_tasks(request):
    tasks = Task.objects.filter(owner=request.user)
    contexto = {
        'tasks':tasks
    }
    return render(request, 'tasks/tasks.html', contexto)


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            if Task.objects.filter(title=task.title, owner=task.owner).exists():
                form.add_error('title', 'Ya tienes una tarea con este título.')
            else:
                task.save()
                messages.add_message(request, messages.SUCCESS, '¡Operación exitosa!', extra_tags='success')
                return redirect('tasks')
        else:
            messages.add_message(request, messages.ERROR, 'Error al crear la tarea. Por favor, revisa el formulario.', extra_tags='danger')
    else:
        form = TaskForm()
    contexto = {
        'form': form,
        'accion': 'Crear una tarea'
    }
    return render(request, 'tasks/task_form.html', contexto)