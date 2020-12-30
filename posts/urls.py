from django.urls import path

from . import views


urlpatterns = [
    path('', views.AllPosts.as_view(), name='all_posts'),
    path('<uuid:pk>/', views.ConcretePost.as_view(), name='concrete_post'),
    path('<uuid:pk>/change/', views.ChangePost.as_view(), name='change_post'),
    path('<uuid:pk>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path(
        'category/<uuid:pk>/', views.CategoryPosts.as_view(),
        name='category_posts'
    ),
    path('search/', views.SearchPosts.as_view(), name='search_posts'),
    path('create/', views.CreatePost.as_view(), name='create_post'),
]
