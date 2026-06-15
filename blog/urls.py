from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('my-posts/', views.my_posts_view, name='my_posts'),

    # create MUST be before <slug:slug>
    path('post/create/', views.post_create_view, name='post_create'),

    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<slug:slug>/like/', views.like_post_view, name='like_post'),
]