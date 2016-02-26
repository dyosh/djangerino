from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login # (Dan): login user right after registering

from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    # (Dan): this method gets calledback after submitting the POST request
    # (Dan): so we do the logic back in this method, should find a way to explicitly call a custom method.
    if request.method == "POST":
        form = PostForm(request.POST) # (Dan): POST returns a request.POST (dict like object)
        if form.is_valid():
            post = form.save(commit=False) #(Dan): ???
            post.author = request.user # (Dan): ???
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        if request.user.is_authenticated():
            form = PostForm()
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return redirect('/', {'posts': posts})

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('post_detail', post_id)

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog.views.post_list') #(Dan): same as just putting 'post_list', this may be more clear.

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', post_id=post_pk)

@login_required
def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('post_detail', post_id=comment.post.pk)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return redirect('/', {'posts': posts})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
