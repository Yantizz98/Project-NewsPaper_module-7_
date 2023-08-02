from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("description")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Содержание новости не должно быть идентично названию."
            )

        return cleaned_data


class ArticleForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'postCategory']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("description")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Содержание новости не должно быть идентично названию."
            )

        return cleaned_data