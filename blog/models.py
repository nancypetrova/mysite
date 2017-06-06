# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class PublichedManadger(models.Manager):
    def get_queryset(self):
        return super(PublichedManadger, self).get_queryset().filter(status='publiched')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('publiched', 'Publiched'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publich')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = RichTextField()
    publich = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # стандартный менеджер
    publiched = PublichedManadger()  # наш менеджер

    class Meta:
        ordering = ('-publich',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publich.year,
                                                 self.publich.strftime('%m'),
                                                 self.publich.strftime('%d'),
                                                 self.slug])
    tags=TaggableManager()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return  'Комментарий от пользователя {} на {}'.format(self.name, self.post)