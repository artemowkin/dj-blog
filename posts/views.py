from django.shortcuts import render, redirect
from django.forms import Form
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

import services.common as services_common
from . import services
from utils.views import DefaultView
from .models import Post
from .forms import PostForm


class AllPosts(DefaultView):
    model = Post
    template_name = 'posts/all_posts.html'

    def get(self, request):
        posts = services_common.get_all_model_entries(self.model)
        return render(request, self.template_name, {'posts': posts})


class ConcretePost(DefaultView):
    model = Post
    template_name = 'posts/concrete_post.html'

    def get(self, request, pk):
        post = services_common.get_concrete_model_entry_by_pk(self.model, pk)
        return render(request, self.template_name, {'post': post})


class SearchPosts(DefaultView):
    template_name = 'posts/search_posts.html'

    def get(self, request):
        query = self.request.GET.get('query', '')
        posts = services.search_posts(query)
        return render(
            request, self.template_name, {'posts': posts, 'query': query}
        )


class CategoryPosts(DefaultView):
    template_name = 'posts/category_posts.html'

    def get(self, request, pk):
        category, posts = services.get_category_posts(pk)
        return render(
            request, self.template_name, {
                'category': category, 'posts': posts
            }
        )


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/create.html'
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ChangePost(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/change.html'
    context_object_name = 'post'
    raise_exception = True


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    raise_exception = True
    success_url = reverse_lazy('all_posts')
