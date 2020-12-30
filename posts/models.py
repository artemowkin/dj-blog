from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

from utils.models import UUIDModel


User = get_user_model()


class Category(UUIDModel):
    """Post category model

    Attributes
    ----------
    title : CharField
        Category title in English. This field is required
    title_ru : CharField
        Category title in Russian. This field isn't required

    """
    title = models.CharField(_('category title in English'), max_length=255)
    title_ru = models.CharField(
        _('category title in Russian'), max_length=255, blank=True
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_posts', args=[str(self.pk)])


class Post(UUIDModel):
    """Model of post

    Attributes
    ----------
    title : CharField
        Post title in English. This field is required
    title_ru : CharField
        Post title in Russian. This field isn't required
    author : ForeignKey[User]
        Post author
    category : ForeignKey[Category]
        Post category
    pub_date : DateTimeField
        Automatic calculating field. Post publishing date and time
    body : HTMLField
        Post body in English
    body_ru : HTMLField
        Post body in Russian

    """

    title = models.CharField(_('title of post in English'), max_length=255)
    title_ru = models.CharField(
        _('title of post in Russian'), max_length=255, blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name=_('post author')
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts',
        verbose_name=_('post category')
    )
    pub_date = models.DateTimeField(auto_now=True)
    body = HTMLField(_('post body in English'))
    body_ru = HTMLField(_('post body in Russian'), blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concrete_post', args=[str(self.pk)])
