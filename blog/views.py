from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views import generic, View
from .models import Post

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    # limits number of post visibile on page to 6
    # if more than 6, django will add page navigation
    paginate_by = 6


class PostDetail(View):
    # in class based views we do operations with POST and GET by defining methods
    def get(self, request, slug, *args, **kwargs):
        # filtering post which are finished (not draft)
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # checking if user liked the post and setting appropriate boolean
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked":liked
            },
        )
