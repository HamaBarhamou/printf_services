from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, Tag, Category
from .forms import PostForm, CommentForm, CategoryForm, TagForm
from django.http import JsonResponse



@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('blog:category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_detail.html', {'category': category, 'page_obj': page_obj})


@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('blog:category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/update_category.html', {'form': form})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('blog:category_list')


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('blog:tag_detail', pk=tag.pk)
    else:
        form = TagForm()
    return render(request, 'blog/create_tag.html', {'form': form})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})


def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = tag.post_set.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'page_obj': page_obj})


@login_required
def update_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('blog:tag_detail', pk=tag.pk)
    else:
        form = TagForm(instance=tag)
    return render(request, 'blog/update_tag.html', {'form': form})


@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('blog:tag_list')
    return render(request, 'blog/delete_tag.html', {'tag': tag})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_list(request):
    search_query = request.GET.get('q')
    if search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def update_post(request, pk):
    # Récupérer le post correspondant à la clé primaire pk
    post = get_object_or_404(Post, pk=pk)
    
    # Vérifier si l'utilisateur connecté est l'auteur du post
    if request.user != post.author:
        # Si l'utilisateur n'est pas l'auteur, afficher un message d'erreur et rediriger vers la page de détails du post
        messages.error(request, 'You are not authorized to update this post!')
        return redirect('blog:post_detail', pk=pk)
    
    # Si la méthode HTTP utilisée est POST, traiter les données du formulaire de mise à jour du post
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Enregistrer les modifications apportées au post
            post = form.save(commit=False)
            post.save()
            # Afficher un message de succès et rediriger vers la page de détails du post mis à jour
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', pk=pk)
    else:
        # Si la méthode HTTP utilisée est GET, afficher le formulaire de mise à jour prérempli avec les données actuelles du post
        form = PostForm(instance=post)
    # Afficher la page de mise à jour du post avec le formulaire de mise à jour
    return render(request, 'blog/update_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post!')
        return redirect('blog:post_detail', pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('blog:post_list')

@login_required
def create_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog:post_detail', pk=comment.post.pk)
    return redirect('blog:post_list')


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, 'You are not authorized to delete this comment!')
        return redirect('blog:post_detail', pk=comment.post.pk)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def like_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            action = 'unliked'
        else:
            comment.likes.add(user)
            action = 'liked'
        likes_count = comment.likes.count()
        return JsonResponse({'status': 'success', 'action': action, 'likes_count': likes_count})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method!'})
