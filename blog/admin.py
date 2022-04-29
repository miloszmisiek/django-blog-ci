from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    
    # prepopulated_fields is a django special propery designed for slug fields
    # uses JS to format and displat slug field
    prepopulated_fields = {'slug': ('title',)}
    #  filter box in the post lists, passing what options to use for filtering
    list_filter = ('status', 'created_on')
    # how posts are displayed in the list
    list_display = ('title', 'slug', 'status', 'created_on')
    # adds search field which searches posts by arguments passed
    search_fields = ['title', 'content']
    summernote_fields = ('content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    # allows to specify different actions from the action drop-down box
    # default action is delete the selected item
    # accepts functions as arguments, so must build one to use it
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        # method updates the queryset approved to True (action call)
        queryset.update(approved=True)