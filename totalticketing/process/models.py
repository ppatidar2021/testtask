from django.db import models
from django.contrib.auth.models import User


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    task_id = models.CharField(max_length=100, blank=False, default="")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} | Task ID: {self.task_id} | Completed: {self.is_completed}"
