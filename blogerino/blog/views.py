from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    # (Dan): this method gets calledback after submitting the POST request
    # (Dan): so we do the logic back in this method, should find a way to explicitly call a custom method.
    if request.method == "POST":
        form = PostForm(request.POST) # (Dan): POST returns a request.POST (dict like object)
        if form.is_valid():
            post = form.save(commit=False) #(Dan): ???
            post.author = request.user # (Dan): ???
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        if request.user.is_authenticated():
            form = PostForm()
        else:
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            return redirect('/', {'posts': posts})

    return render(request, 'blog/post_edit.html', {'form': form})

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
