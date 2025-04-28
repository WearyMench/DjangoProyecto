"""Este es donde se hacen las vistas de las paginas."""
from django.http import HttpResponse, HttpResponseForbidden
from .models import Project, Task
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .forms import ProjectForm, TaskForm, CustomUserCreationForm, LoginForm

# Create your views here.

def landing_page(request):
    return render(request, 'myapp/landing.html')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to My Projects App.')
            return redirect('projects_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('projects_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def projects_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = Task.objects.filter(project=project)
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            try:
                project.save()
                messages.success(request, 'Project created successfully!')
                return redirect('projects_list')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form, 'project': project})

@login_required
@require_http_methods(["GET", "POST"])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user owns the project this task belongs to
    if task.project.user != request.user:
        messages.error(request, "You don't have permission to edit this task.")
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required
@require_http_methods(["GET", "POST"])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Check if user owns the project this task belongs to
    if task.project.user != request.user:
        messages.error(request, "You don't have permission to delete this task.")
        return HttpResponseForbidden()
    
    if request.method == "POST":
        project_id = task.project.id
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('project_detail', project_id=project_id)
    return render(request, 'delete_task.html', {'task': task})

@login_required
@require_http_methods(["GET", "POST"])
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
@require_http_methods(["GET", "POST"])
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('projects_list')
    return render(request, 'delete_project.html', {'project': project})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('landing_page')

@login_required
def profile(request):
    """View for user profile page"""
    user = request.user
    projects = Project.objects.filter(user=user)
    tasks = Task.objects.filter(project__in=projects)
    
    context = {
        'user': user,
        'projects_count': projects.count(),
        'tasks_count': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count(),
    }
    return render(request, 'myapp/profile.html', context)
