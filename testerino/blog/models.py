from django.db import models
from django.utils import timezone

# creates a table called Post
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now())

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

