from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string

from .models import PostCategory, Subscription


# @receiver(post_save, sender=PostCategory)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новая публикация в вашей любимой категории {instance.category}'
#
#     text_content = (
#         f'Публикация: {instance.name}\n'
#         f'Автор: {instance.author}\n\n'
#         f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Публикация: {instance.name}<br>'
#         f'Автор: {instance.author}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на публикацию</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()

def send_notifications(preview, pk, title, subscribes):
    html_context = render_to_string(
        'account/email/new_post.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/content/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribes,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def new_post_notification(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribes: list[str] = []
        print(f'{subscribes = }')

        for cat in categories:
            subscribes = Subscription.objects.filter(category=cat)
            subscribes += [subs.user.email for subs in subscribes]
        print(f'{subscribes = }')

        send_notifications(instance.preview(), instance.pk, instance.title, subscribes)
