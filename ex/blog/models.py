from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Модель для представления поста (публикации)
class Post(models.Model):
    title = models.CharField(max_length=255)  # Заголовок поста
    content = models.TextField()  # Содержание поста
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем (автором)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста

# Модель для представления комментария к посту
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Связь с постом, к которому относится комментарий
    text = models.TextField()  # Текст комментария
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем (автором комментария)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания комментария

# Модель для расширения стандартной модели пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с пользователем
    bio = models.TextField(blank=True)  # Дополнительная информация о пользователе (биография)

# Сигналы для автоматического создания и сохранения профиля пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
