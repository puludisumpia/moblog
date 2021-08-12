from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Contact, Post, Comment

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("corps",)
    list_display = ("title", "author", "status", "created_on",)
    list_filter = ("created_on", "status",)
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    pass
