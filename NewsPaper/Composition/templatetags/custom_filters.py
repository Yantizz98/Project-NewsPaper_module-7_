from django import template

register = template.Library()

bad_words = ['science', 'from', 'health']


@register.filter()
def censor(content):
    text = content.split()
    for i, word in enumerate(text):
        if word in bad_words:
            text[i] = word[0] + '***'
    return ' '.join(text)
