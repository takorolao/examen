from django.urls import path, re_path
from . import views
from .views import login_view, register_view, post_form, home, logout_view, edit_post, delete_post

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    re_path(r'^posts/(?P<post_id>\d+)/$', views.PostDetailView.as_view(), name='post-detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('posts/new/', post_form, name='create-post'),
    path('posts/<int:post_id>/edit/', post_form, name='edit-post'),
    path('', home, name ='home'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:post_id>/edit/', edit_post, name='edit-post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete-post'),
]
