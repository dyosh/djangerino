from django.contrib import admin
from blog.models import Post
from todolist.models import TodoItem

admin.site.register(Post)
admin.site.register(TodoItem)