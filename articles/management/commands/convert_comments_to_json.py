import json
from django.core.management.base import BaseCommand
from articles.models import Comment  # Замените "myapp" на имя вашего приложения


class Command(BaseCommand):
    help = 'Converts comments to JSON and saves to a file'

    def handle(self, *args, **options):
        comments = Comment.objects.all()

        data = []
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'article_id': comment.article.id,
                'author_name': comment.author_name,
                'comment_text': comment.comment_text,
                'image': str(comment.image) if comment.image else None,
            }
            data.append(comment_data)

        output_file = 'comments.json'
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Successfully converted comments to {output_file}'))