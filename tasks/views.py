from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm
from .models import Task


# Create your views here.
@login_required
def tasks_get_all(request):
    # Filtro desde la solicitud GET, por defecto es 'all'
    filter_by = request.GET.get('filter', 'all')
    if filter_by == 'completed':
        tasks = Task.get_completed_tasks(owner=request.user)
    elif filter_by == 'pending':
        tasks = Task.get_pending_tasks(owner=request.user)
    else:
        tasks = Task.objects.filter(owner=request.user)
    contexto = {'tasks': tasks, 'filter_by': filter_by}
    return render(request, 'tasks/tasks.html', contexto)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            if Task.objects.filter(title=task.title, owner=task.owner).exists():
                form.add_error('title', 'Ya tienes una tarea con este título.')
            else:
                task.save()
                messages.add_message(request, messages.SUCCESS, 'Se creo la nueva tarea con exito!', extra_tags='success')
                return redirect('tasks')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al crear la tarea. Por favor, revisa el formulario.',
                extra_tags='danger',
            )
    else:
        form = TaskForm()
    contexto = {'form': form, 'accion': 'Crear una tarea'}
    return render(request, 'tasks/task_form.html', contexto)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if (request.method == 'POST'):
        task.toggle_completion()
        messages.add_message(request, messages.SUCCESS, 'Se actualizo el estado con exito!', extra_tags='success')
        return redirect('task_detail', task_id=task.id)
    contexto = {'task': task}
    return render(request, 'tasks/task_detail.html', contexto)



@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    if (request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if Task.objects.filter(title=task.title, owner=task.owner).exists():
                form.add_error('title', 'Ya tienes una tarea con este título.')
            else:
                task.save()
                messages.add_message(request, messages.SUCCESS, 'Se edito la tarea con exito!', extra_tags='success')
                return redirect('tasks')
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    contexto = {'form': form, 'accion': 'Editar tarea'}
    return render(request, 'tasks/task_form.html', contexto)


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, owner=request.user)
    messages.add_message(request, messages.SUCCESS, 'Se ha eliminado la tarea con exito!', extra_tags='success')
    task.delete()
    return redirect('tasks')