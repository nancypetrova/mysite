# -*- coding: utf-8 -*-

from django.contrib import admin

from blog.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """
    list_display - обображение полей в админке
    list_filter - по каким поялм фильтровать
    search_fields - поле для поиска и где искать
    prepopulated_fields - автозаполнение поля slug, при написании заголовка
    date_hierarchy - упорядочили по статусу
    ordering - сортировка
    """
    list_display = ('title', 'slug', 'author', 'publich', 'status',)
    list_filter = ('status', 'created', 'publich', 'author',)
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publich'
    ordering = ['status', 'publich', ]


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
# Register your models here.
