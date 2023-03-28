from django.urls import path
from .views import post_list, post_detail, create_post, update_post, delete_post

app_name = 'blog'

urlpatterns = [
    path('post_list', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:pk>/edit/', update_post, name='update_post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
]
