from django.db import models

# Create your models here.
class TodoList(models.Model):
    list_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.list_name}"

class TodoItem(models.Model):
    title = models.CharField(max_length=255)
    due_date=models.DateTimeField()
    checked = models.BooleanField(False)

    todo_list = models.ForeignKey(to=TodoList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}:{self.due_date}"