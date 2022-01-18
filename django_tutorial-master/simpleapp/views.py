from django.views.generic import ListView, DetailView
from .models import Article
from django.views import View
from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator
from .filters import ArticleFilter# импортируем класс, позволяющий удобно осуществлять постраничный вывод

# Create your views here.

# В отличие от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов (например гет или пост, вспоминаем реквесты из модуля C5)
class Articles(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'
    ordering = ['-title']
    paginate_by = 1

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ArticleFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

class ArticleList(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'
    queryset = Article.objects.order_by('-datetime')

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'

