from django import forms

from .models import Post, Category


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label=None
    )

    class Meta:
        model = Post
        fields = ('title', 'title_ru', 'category', 'body', 'body_ru')
