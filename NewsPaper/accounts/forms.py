# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group


# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         site_users = Group.objects.get(name="site users")
#         user.groups.add(site_users)
#         return user

from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать в наш новостной канал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_admins(
        subject='Новый пользователь!',
        message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user


