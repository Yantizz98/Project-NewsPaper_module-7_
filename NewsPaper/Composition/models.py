from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

NEWS = 'NW'
ARTICLE = 'AR'

POST_TYPES = [(ARTICLE, 'Статья'), (NEWS, 'Новость')]


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(postRating=Sum('postRating'))
        p_rat = 0
        p_rat += post_rat.get('postRating')

        comment_rat = self.authorUser.comment_set.aggregate(commentRating=Sum('commRating'))
        c_rat = 0
        c_rat += comment_rat.get('commentRating')

        self.authorRating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)
    subscribes = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass

    def get_category(self):
        return self.categoryName

    def __str__(self):
        return f' Категория: {self.categoryName.title()}'


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    postType = models.CharField(max_length=2, choices=POST_TYPES, default=NEWS)
    addTime = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField("Category", through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    postRating = models.SmallIntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.content[0:124] + '...'

    def __str__(self):
        return f'{self.postType.title()}: {self.title.title()}, Автор: {self.author}, Категория: {self.postCategory}, Рейтинг: {self.postRating}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    commRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commRating += 1
        self.save()

    def dislike(self):
        self.commRating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    category = models.ForeignKey(
        to='PostCategory',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )













