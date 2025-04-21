"""Este es donde se hacen las vistas de las paginas."""
from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import render, get_object_or_404, redirect
from django import forms

# Create your views here.

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks, 'form': form})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects_list')
    else:
        form = ProjectForm()
    
    return render(request, 'create_project.html', {'form': form})

# Editar una tarea
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'edit_task.html', {'form': form, 'task': task})

# Eliminar una tarea
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id
    task.delete()
    return redirect('project_detail', project_id=project_id)

# Editar un proyecto
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects_list')
    return render(request, 'edit_project.html', {'form': form, 'project': project})

# Eliminar un proyecto
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('projects_list')
