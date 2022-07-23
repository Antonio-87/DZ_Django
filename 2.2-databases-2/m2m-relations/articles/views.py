from django.shortcuts import render
from django.db.models.query import Prefetch
from articles.models import Article, ArticleScope, Tag


def articles_list(request):
    template = 'articles/news.html'
    tag = request.GET.get('tag')
    tag_list = Tag.objects.all().order_by('name')
    if tag:
        object_list = Article.objects.filter(tag=tag).order_by('-published_at').prefetch_related(
            Prefetch('scopes', ArticleScope.objects.order_by('-is_main', 'tag__name'))
        )
    else:
        object_list = Article.objects.order_by('-published_at').prefetch_related(
            Prefetch('scopes', ArticleScope.objects.order_by('-is_main', 'tag__name'))
        )
    context = {
                'object_list': object_list,
                'tag_list': tag_list
    }
    return render(request, template, context)
