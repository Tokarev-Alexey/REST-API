from django.contrib import admin

from posts.models import Post, Comment


class CommentFilter(admin.ModelAdmin):
    # Поля, которые отображаются в списке
    list_display = ('post', 'author_comm', 'text_comm', 'pub_date')
    # !!! ВКЛЮЧАЕМ ФИЛЬТРАЦИЮ ЗДЕСЬ !!!
    list_filter = ('post', 'author_comm')  # Фильтры по полям `post` и `author`
    search_fields = ('text_comm',)

class PostFilter(admin.ModelAdmin):
    # Поля, которые отображаются в списке
    list_display = ('title', 'author', 'text', 'pub_date')
    # !!! ВКЛЮЧАЕМ ФИЛЬТРАЦИЮ ЗДЕСЬ !!!
    list_filter = ('author', 'pub_date')
    search_fields = ('title',)

admin.site.register(Comment, CommentFilter)
admin.site.register(Post, PostFilter)
