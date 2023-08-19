from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Task(models.Model):
    priority = [
        ("High", 'High'),
        ("Medium", 'Medium'),
        ("Low", 'Low'),
    ]
    status_choice = [
        ("active", "active"),
        ("completed", "completed"),
        ("expired", "expired"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=status_choice, default="active")
    title = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default="12-12-2024")
    due_time = models.TimeField(default="15:14:23")
    priority = models.CharField(
        max_length=7,
        choices=priority,
        default="Medium",
    )
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.owner.username}'s task titled {self.title}"