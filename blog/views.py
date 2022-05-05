from django.shortcuts import get_object_or_404, render, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm
from django.contrib import messages

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
                "commented": False,
                "liked":liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        # filtering post which are finished (not draft)
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        # checking if user liked the post and setting appropriate boolean
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # this will get all the data posted in the form
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # saving comment_form with passed data to variable
            # no commit is passed to first connect it to the post instance
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Submited successfully!.')
        else:
            # if user is not authenticated the empty comment form will be passed
            comment_form = CommentForm()
        
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked":liked,
                "comment_form": CommentForm(),
            },
        )

class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        # new response type to reload post_detail view
        # reverse shortcut gives ability to look up for url name(given in urls.py)
        # args is what comes in url, so slug will be pasted '.../<slug>/'
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))