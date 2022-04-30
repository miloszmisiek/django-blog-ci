import imp
from re import template
from django.shortcuts import render
from django.views import generic
from .models import Post

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    # limits number of post visibile on page to 6
    # if more than 6, django will add page navigation
    paginate_by = 6