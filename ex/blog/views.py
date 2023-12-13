from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

def login_view(request):
    """
    Обработка входа пользователя.

    GET: Отображает форму входа.
    POST: Проверяет данные формы, в случае успеха входит и перенаправляет на 'post-list'.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('post-list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    """
    Обработка регистрации нового пользователя.

    GET: Отображает форму регистрации.
    POST: Проверяет данные формы, в случае успеха регистрирует пользователя и входит,
    затем перенаправляет на 'post-list'.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class PostListView(View):
    """
    Представление для списка постов.

    GET: Отображает список постов с пагинацией.
    POST: Обрабатывает комментарии к постам.
    """
    template_name = 'blog/post_list.html'
    paginate_by = 5  # Количество постов на странице

    def get(self, request):
        all_posts = Post.objects.all()

        # Настраиваем пагинацию
        paginator = Paginator(all_posts, self.paginate_by)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'posts': posts})

    def post(self, request):
        """
        Обработка комментариев к постам.

        POST: Добавляет комментарий к выбранному посту.
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            # Создание комментария
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, pk=post_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен.')
        else:
            messages.error(request, 'Ошибка валидации формы комментария.')

        return redirect('post-detail', post_id=post_id)

class PostDetailView(View):
    """
    Представление для деталей поста.

    GET: Отображает детали поста и комментарии к нему.
    POST: Обрабатывает комментарии к посту.
    """
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()  # Инициализация формы для добавления комментария
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

    def post(self, request, post_id):
        """
        Обработка комментариев к посту.

        POST: Добавляет комментарий к выбранному посту.
        """
        form = CommentForm(request.POST)
        if form.is_valid():
            # Создание комментария
            post = get_object_or_404(Post, pk=post_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен.')
        else:
            messages.error(request, 'Ошибка валидации формы комментария.')

        return redirect('post-detail', post_id=post_id)

def home(request):
    """
    Отображает домашнюю страницу.
    """
    return render(request, 'home.html')

def post_form(request):
    """
    Обработка формы для создания нового поста.

    GET: Отображает форму создания поста.
    POST: Создает новый пост и перенаправляет на 'post-list'.
    """
    post = None  # Объявление переменной post перед использованием
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Создание новой публикации
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-list')
    else:
        form = PostForm()

    return render(request, 'post_form.html', {'form': form, 'post': post})

@login_required
def logout_view(request):
    """
    Обработка выхода пользователя.

    GET: Выходит пользователя и перенаправляет на 'home'.
    """
    logout(request)
    return redirect('home')

@login_required
def edit_post(request, post_id):
    """
    Обработка редактирования поста.

    GET: Отображает форму редактирования поста.
    POST: Обрабатывает данные формы, редактирует пост и перенаправляет на 'post-detail'.
    """
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно отредактирован.')
            return redirect('post-detail', post_id=post.id)
        else:
            messages.error(request, 'Ошибка валидации формы редактирования поста.')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    """
    Обработка удаления поста.

    GET: Удаляет выбранный пост и перенаправляет на 'post-list'.
    """
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Пост успешно удален.')
    return redirect('post-list')
