from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import escape

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Keep nullable for migration
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'user']
        ordering = ['-updated_at']

    def clean(self):
        # Check if user has reached project limit
        if self.user and self.user.project_set.count() >= 100:  # Limit to 100 projects per user
            raise ValidationError('You have reached the maximum number of projects (100).')
        
        # Sanitize input
        self.name = escape(self.name.strip())
        if self.description:
            self.description = escape(self.description.strip())

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call clean() and validate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user.username if self.user else 'No user'})"

    def get_tasks_count(self):
        return self.task_set.count()

    def get_completed_tasks_count(self):
        return self.task_set.filter(status='done').count()


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def clean(self):
        # Validate due date
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError('Due date cannot be in the past.')
        
        # Sanitize input
        self.title = escape(self.title.strip())
        self.description = escape(self.description.strip())
        
        # Validate status
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError('Invalid status value.')

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call clean() and validate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_overdue(self):
        return bool(self.due_date and self.due_date < timezone.now() and self.status != 'done')
