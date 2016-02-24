from django.db import models

class TodoItem(models.Model):
    content = models.CharField(max_length=500)
    date = models.DateTimeField()

    def __str__(self):
        return self.item