from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200)


class Task(models.Model):
    STATUS_CHOICES = [
        ('PEND', 'Pendiente'),
        ('PROG', 'En Progreso'),
        ('DONE', 'Completada'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PEND')

    def __str__(self):
        return self.title
