from django.conf.urls import url, include
from django.views.generic import ListView
from todolist.models import TodoItem

urlpatterns = [
    url(r'^$', ListView.as_view(queryset=TodoItem.objects.all().order_by("-date"),
        template_name="todolist/todolist.html")),
]