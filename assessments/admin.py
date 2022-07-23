from django.contrib import admin
from .models import Log, Comment, Message


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
   list_display = ('author', 'document', 'created')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
   list_display = ('log', 'body', 'author', 'created')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
   list_display = ('message_from', 'message_to', 'body', 'created')

