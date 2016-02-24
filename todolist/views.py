from django.shortcuts import render

def todolist(request):
    return render(request, 'todolist/todolist.html')