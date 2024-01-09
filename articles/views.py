import datetime

from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Article, Comment
from .pagination import CommentsPagination, ArticlesPagination
from .serializers import CommentsSerializer, ArticlesSerializer


def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})


def detail(request, article_id):
    try:
        a = Article.objects.get(id=article_id)


    except:
        raise Http404("Статья не найдена")

    latest_comments_list = a.comment_set.order_by('id')[:10]

    return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list})


def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)

    except:
        raise Http404("Статья не найдена")

    comment = a.comment_set.create(author_name=request.POST['username'], comment_text=request.POST['comment'])
    if 'image' in request.FILES:
        comment.image = request.FILES['image']
        comment.save()

    return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))


def delete_comment(request, article_id, comment_id):
    try:
        article = Article.objects.get(id=article_id)
        comment = Comment.objects.get(id=comment_id)

    except:
        raise Http404("Комментарий не найден")

    comment.delete()

    return HttpResponseRedirect(reverse('articles:detail', args=(article.id,)))


def detail_comment(request, article_id, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        article = Article.objects.get(id=article_id)

    except:
        raise Http404("comment не найден")

    return render(request, 'articles/detail_comment.html', {'comment': comment, 'article': article})


def edit_comment(request, article_id, comment_id):
    try:
        article = Article.objects.get(id=article_id)
        comment = Comment.objects.get(id=comment_id)
    except:
        raise Http404("Комментарий к статье не найден")
    if 'image' in request.FILES:
        comment.image = request.FILES['image']
        comment.save()
    comment.comment_text = request.POST['comment']
    comment.save()
    return HttpResponseRedirect(reverse('articles:detail_comment', args=(article.id, comment.id,)))


class ArticlesViewSet(ModelViewSet):
    serializer_class = ArticlesSerializer
    pagination_class = ArticlesPagination
    queryset = Article.objects.all()


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.username == 'moderator'
    

class CurrentUserArticlesViewSet(ModelViewSet):
    serializer_class = ArticlesSerializer
    pagination_class = ArticlesPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator]
    queryset = Article.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(
            Q(author__username=user.username) | (Q(author__username='moderator') & Q(
                pub_date__gte=timezone.now() - datetime.timedelta(days=7))))


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = CommentsPagination
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['article']

    def create(self, request, *args, **kwargs):
        user = self.request.user
        comment_data = request.data
        comment_data['author'] = user.id
        serializer = self.get_serializer(data=comment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        excluded_word = 'badword'
        return Comment.objects.filter(~Q(comment_text__icontains=excluded_word))