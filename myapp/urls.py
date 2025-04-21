from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('create-project/', views.create_project, name='create_project'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
]
