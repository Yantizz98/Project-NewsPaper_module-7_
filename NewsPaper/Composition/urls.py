from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(),name='article_create'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    # path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
    # path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
    # path('unsubscribe/<int:pk>/', unsubscribe_to_category, name='unsubscribe'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    # path('test/', IndexView.as_view(),),
]
