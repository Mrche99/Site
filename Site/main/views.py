from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import News
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class ShowNewsView(ListView):
    model = News
    template_name = 'main/Home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 2
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ShowNewsView, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта '
        return ctx

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'post'
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(NewsDetailView, self).get_context_data(**kwargs)
        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        return ctx

class CreateNewsView(CreateView, LoginRequiredMixin):
    model = News
    template_name = 'main/create_news.html'

    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateNewsView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = News
    template_name = 'main/create_news.html'
    fields = ['title', 'text']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(UpdateNewsView, self).get_context_data(**kwargs)
        ctx['title'] ='Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class DeleteNewsView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = News
    success_url = '/'
    template_name = 'main/delete_news.html'
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

def contacts(request):
    return render(request, 'main/Contacts.html', {'title': 'Страница контактов!'})

class UserAllNewsView(ListView):
    model = News
    template_name = 'main/user_news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')


    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(UserAllNewsView, self).get_context_data(**kwargs)
        ctx['title'] = f'Статья от пользователя{self.kwargs.get("username")}'
        return ctx