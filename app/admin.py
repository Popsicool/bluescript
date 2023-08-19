from django.contrib import admin
from .models import TaskCategory, Task

# Register your models here.

admin.site.register(TaskCategory)
admin.site.register(Task)
