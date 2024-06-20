from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from newspaper.models import Article
from users.models import User


def get_weeks_best_article():
    best_article = Article.objects.all()[:10]
    return best_article


def send_weekly_best_article_email():
    users = User.objects.all()
    article = get_weeks_best_article()
    for user in users:
        subject = "Лучшие записи этой недели!"
        html_message = render_to_string('emails/weekly_best_articles.html', {'article': article, 'user': user})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = user.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task
def weekly_best_article_email_task():
    send_weekly_best_article_email()
