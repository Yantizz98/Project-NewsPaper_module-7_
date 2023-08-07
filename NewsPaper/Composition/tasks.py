from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from Composition.models import Category, Post


@shared_task
def with_every_new_post(postCategory, preview, title, emails, get_absolute_url):

    subject = f'Новая запись в категории {postCategory}'

    text_content = (
        f'Название: {title}\n'
        f'Анонс: {preview}\n\n'
        f'Ссылка на публикацию: {settings.SITE_URL}{get_absolute_url}'
    )
    html_content = (
        f'Название: {title}<br>'
        f'Анонс: {preview}<br><br>'
        f'<a href="{settings.SITE_URL}{get_absolute_url}">'
        f'Ссылка на публикацию</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_newsletter():
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(addTime__gte=last_week)
    print(f'{posts}')
    users = User.objects.all().values_list('email', flat=True)
    categories = set(posts.values_list('postCategory__categoryName', flat=True))
    subscribers = set(Category.objects.filter(categoryName__in=categories).values_list('subscribes__email', flat=True))
    html_content = render_to_string(
        'account/email/weekly_newsletter.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()