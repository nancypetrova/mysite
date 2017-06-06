# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailPostForm, ComentForm


def post_list(request, tag_slug=None):  # сюда добавлено в этом уроке tag_slug=None
    object_list = Post.publiched.all()

    # добавлен код для меток в этом уроке
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # End добавлен код для меток

    paginator = Paginator(object_list, 3)  # выводить по 3 результата
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # официально класс говорит, если страница не является цнелым числом, поставить первую страницу
        # простыми словами класс говорит, разработчик укажи, что отображать первым
        posts = paginator.page(1)
    except EmptyPage:
        # что показать, если страница выходит за диапозон, то последнюю
        # то есть так 1 из 30 (при условии что всего 30 страниц)
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


# добавили также в словарь 'tag':  tag в этом уроке




def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='publiched',
                             publich__year=year,
                             publich__month=month,
                             publich__day=day)
    # Список активных комментариев для этого сообщения
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # Был отправлен комментарий
        comment_form = ComentForm(data=request.POST)
        if comment_form.is_valid():
            # Создать объект Comment, но не сохранять в базе данных
            new_comment = comment_form.save(commit=False)
            # Присвоить текущую запись комментарию
            new_comment.post = post
            # Сохранить комментарий к базе данных
            new_comment.save()

    else:
        comment_form = ComentForm()

    # выбираем все теги
    post_tags_ids = post.tags.values_list('id', flat=True)
    # все записи содержащие ранее выбранные теги, исключаем запись которая открыта
    similar_posts = Post.publiched.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # создаём счётчик для вывода рекомендуемых записей
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publich')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts, })


def post_share(request, post_id):
    # получить запись по id
    post = get_object_or_404(Post, id=post_id, status='publiched')
    sent = False
    if request.method == 'POST':
        # форма была представлена
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # поля формы прошли проверку
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендую к прочтению "{}"'.format(cd['name'], cd['email'], post.title)

            message = 'Читать "{}" at {}\n\n{}\'s комментарий: {}'.format(post.title, post_url, cd['name'],
                                                                          cd['comments'])

            send_mail(subject, message, 'pythontestsmail@gmail.com', [cd['to']])

            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
