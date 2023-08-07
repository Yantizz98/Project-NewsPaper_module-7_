from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription, PostCategory
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class NewsList(ListView):
    model = Post
    ordering = 'addTime'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_time'] = Post.addTime
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class PostSearch(ListView):
    form_class = PostFilter
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_time'] = Post.addTime
        context['filterset'] = self.filterset
        return context


# def create_news(request):
#     form = NewsForm()
#
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'news_create.html', {'form': form})

class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('Composition.add_post',)
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.postType = 'NW'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('Composition.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.postType = 'NW'
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('Composition.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('Composition.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.postType = 'AR'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('Composition.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.postType = 'AR'
        return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('Composition.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


# class PostCategoryView(ListView):
#     model = Post
#     template_name = 'category.html'
#     context_object_name = 'posts'
#     ordering = ['-addTime']
#     paginate_by = 10
#
#     def get_queryset(self):
#         self.id = resolve(self.request.path_info).kwargs['pk']
#         c = Category.objects.get(id=self.id)
#         queryset = Post.objects.filter(postCategory=c)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         category = Category.objects.get(id=self.id)
#         subscribed = category.subscribes.filter(email=user.email)
#         if not subscribed:
#             context['category'] = category
#
#         return context


# @login_required
# def subscribe_to_category(self, pk):
#     global email, html
#     user = self.user
#     category = Category.objects.get(id=pk)
#
#     if not category.subscribes.filter(id=user.id).exists():
#         category.subscribes.add(user)
#         email = user.email
#         html = render_to_string(
#             'email/subscribed.hnml',
#             {
#                 'category': category,
#                 'user': user
#             },
#         )
#
#     msg = EmailMultiAlternatives(
#         subject=f'{category} subscriptions',
#         body='',
#         from_email='DEFAULT_FROM_EMAIL',
#         to=[email, ],
#     )
#     msg.attach_alternative(html, 'text/html')
#
#     try:
#         msg.send()
#     except Exception as e:
#         print(e)
#         return redirect('/content/')
#     return redirect('/content/')
#
#
# @login_required
# def unsubscribe_to_category(self, pk):
#     user = self.user
#     c = Category.objects.get(id=pk)
#
#     if c.subscribes.filter(id=user.id).exists():
#         c.subscribes.remove(user)
#     return redirect('/content/')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('categoryName')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


# from django.http import HttpResponse
# from django.views import View
# from .tasks import hello, printer
#
#
# # class IndexView(View):
# #     def get(self, request):
# #         hello.delay()
# #         return HttpResponse('Hello!')
#
# class IndexView(View):
#     def get(self, request):
#         printer.delay(10)
#         hello.delay()
#         return HttpResponse('Hello!')