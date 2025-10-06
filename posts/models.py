from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', )
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_comm = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_comm = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return f' комментарий {self.post, self.author_comm, self.pub_date}'

